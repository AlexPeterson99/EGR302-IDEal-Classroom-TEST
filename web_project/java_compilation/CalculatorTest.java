/**
 * Created By: Alex Peterson
 * Last Edited: Feb 7, 2020
 * 
 * Dependencies: 
 *      "./java_dependencies/junit-4.13.jar"
 *      "./java_dependencies/hamcrest-core-1.3.jar"
 * 
 * Description: 
 *      CalculatorTest.java is a test class used as an example JAVA class for compilation.
 * Compiled and tests Calculator.java
 */
import static org.junit.Assert.assertEquals;
import org.junit.Test;

public class CalculatorTest {
  @Test
  public void evaluatesExpression() {
    Calculator calculator = new Calculator();
    int sum = calculator.evaluate("1+2+3");
    assertEquals(6, sum);
  }
}