import Ast.{AstElem, AstNodeList}
/**
  * Type for select propositions
  */
object SelectProp extends Ast.AstSumNode {
  /**
    * Specifies the argument types for this sum operation
    *
    * @return the list of arguments
    */
  override protected def args: List[AstElem] = List(Star, AstNodeList(ConcreteSelectProp))
}
