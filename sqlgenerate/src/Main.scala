/**
  * Created by tianyuli on 3/1/17.
  */
object Main {
  def main(args : Array[String]) : Unit =
    new SimpleSelect()
      .generateValues(Context(Map("foo" -> List("a1", "a2"), "bar" -> List("b1")), Set()))
      .map(_._1)
      .foreach(println)
}
