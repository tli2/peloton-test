import Ast.AstElem

/**
  * Type for elements allowed in a FROM clause
  */
object FromClass extends AstElem {
  override def generateValues(context: Context): Iterator[Ast.Clause] =
    context.schema.keySet.map(a => (a, context.addTableToScope(a))).iterator
}
