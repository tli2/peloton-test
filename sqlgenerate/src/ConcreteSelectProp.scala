import Ast.AstElem

/**
  * Type for concrete Select propositions
  */
object ConcreteSelectProp extends AstElem {
  override def generateValues(context: Context): Iterator[Ast.Clause] =
    context.schema
      .filterKeys(context.scope.contains)
      .mapValues(_.iterator)
      .valuesIterator
      .reduceLeft((a, b) => a ++ b)
      .map(a => (a, context))
}
