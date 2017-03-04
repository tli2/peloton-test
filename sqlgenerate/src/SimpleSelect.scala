import Ast.AstElem
/**
  * SELECT [] FROM []
  */
class SimpleSelect extends Ast.AstProductNode {
  override def args: List[AstElem] = List(Ast.AstNodeList(FromClass), SelectProp)

  override def format(args: List[String]): String =
    if (args.length != 2)
      throw new IllegalArgumentException
    else
      String.format("SELECT %s FROM %s", args(1), args.head)
}
