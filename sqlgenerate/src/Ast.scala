
/**
  * Created by tianyuli on 2/27/17.
  */
object Ast {

  type Clause = (String, Context)


  trait AstElem  {
    /**
      * Iterate through all the possible values of this type, given a language context
      * @param context the surrounding context of this element
      * @return an Iterator to all possible Strings of this type, and the resulting new context
      */
    def generateValues(context : Context) : Iterator[Clause]
  }

  /**
    * For Ast elements that is formed by taking a conjunction of ast elements. (e.g. + is one such element)
    */
  abstract class AstProductNode extends AstElem {
    /**
      * Specifies the argument types for this product operation
      * @return the list of arguments, note that elements that appear prior in the list are not allowed to depend
      *         on the context of a latter element
      */
    protected def args : List[AstElem]

    /**
      * Constructs the actual String for this element given a list of strings for the arguments
      * @param args Values of the argument type, in the same order as declared in args
      * @return the string representation of this element
      */
    protected def format(args: List[String]): String

    override def generateValues (context : Context) : Iterator[Clause] = astProductIterator(context, args, format)
  }

  /**
    * For Ast elements that is formed by taking a disjunction of ast elements
    * (e.g. a select proposition can be either a * or a column name)
    */
  abstract class AstSumNode extends AstElem {
    /**
      * Specifies the argument types for this sum operation
      * @return the list of arguments
      */
    protected def args : List[AstElem]

    override def generateValues(context: Context): Iterator[Clause] = astSumIterator(context, args)
  }

  /**
    * For Ast elements that is a list type of another ast element. Note that this is simply an optimization instead of
    * a recursive product definition
    * @param listType the type of elem this element takes
    */
  case class AstNodeList(listType : AstElem) extends AstElem {
    override def generateValues(context: Context): Iterator[Clause] =
      Combinations.combinations(listType.generateValues(context).toVector)
        .map(a => connectListClauses(context, a))
  }


  // toIterate must be non-empty
  private def astProductIterator(context: Context,
                                 toIterate: List[AstElem],
                                 formatter: List[String] => String): Iterator[Clause] = {

    def recursiveProductIterator(context : Context, toIterate : List[AstElem])
    : Iterator[(List[String], Context)] = toIterate match {
      case Nil => throw new IllegalArgumentException
      case x :: Nil => x.generateValues(context).map(a => (List(a._1), a._2))
      case x :: xs =>
        x.generateValues(context)
          .map(a => recursiveProductIterator(a._2, xs).map(b => (a._1 :: b._1, b._2)))
          .reduceLeft((a: Iterator[(List[String], Context)], b) => a ++ b)
    }

    recursiveProductIterator(context, toIterate).map(a => (formatter(a._1), a._2))
  }

  private def astSumIterator(context : Context, toIterate : List[AstElem])  : Iterator[Clause] =
    toIterate.map(_.generateValues(context))
      .fold(Iterator.empty) ((a, b) => a ++ b)


  private[this] def connectListClauses(context: Context, clauses: Vector[Clause]): Clause =
    clauses.foldLeft(("", context))((acc, elem) => (acc._1 + "," + elem._1, acc._2.union(elem._2)))
}
