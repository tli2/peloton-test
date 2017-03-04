/**
  * Created by tianyuli on 3/1/17.
  */
case class Context(schema : Map[String, List[String]], scope : Set[String] ) {

  def addTableToScope(dbName : String) : Context = Context(schema, scope.+(dbName))

  def union (that : Context) : Context =
    if (schema != that.schema)
      throw new IllegalArgumentException("can only union contexts under the same schema")
    else
      Context(schema, scope.union(that.scope))
}
