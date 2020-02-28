/**
 * Created By: Alex Peterson
 * Last Edited: Feb 7, 2020
 * 
 * Dependencies: 
 *      "./java_dependencies/junit-4.13.jar"
 *      "./java_dependencies/hamcrest-core-1.3.jar"
 * 
 * Description: 
 *      Calculator.java is a class used as an example JAVA class for compilation.
 * Compiled and tested against CalculatorTest.java.
 *          
 */

public class Calculator {
    public int evaluate(String expression) {
      int sum = 0;
      for (String summand: expression.split("\\+"))
        sum += Integer.valueOf(summand);
      return sum;
    }
  }