
/**
  * Generates combinations
  */
object Combinations {

  // For now, only support up to 64 elements, returns all non-empty combinations
  def combinations[E](target: Vector[E]): Iterator[Vector[E]] = new CombinationsIterator[E](target)

  private class CombinationsIterator[E](target : Vector[E]) extends Iterator[Vector[E]] {
    require(target.length <= 64 /* size of long in scala */)
    // Number of combinations
    val elements : Long = ~(-1L << target.length)
    var curr : Long = 0L
    override def hasNext(): Boolean = curr < elements

    override def next(): Vector[E] = {
      curr += 1L
      target.zipWithIndex.filter(a => inCombination(a._2)).map(_._1)
    }

    private def inCombination(index : Int) : Boolean =
      ((curr >> index) & 1L) == 1L
  }

}

