import Ast.AstElem

/**
  * Type for the * operator
  */
object Star extends AstElem {
  override def generateValues(context: Context): Iterator[(String, Context)] = Iterator.single(("*", context))
}
