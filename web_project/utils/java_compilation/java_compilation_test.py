import unittest
import compile

class TestJavaCompilation(unittest.TestCase):

    def test_test(self):
        print('oof')
        #with self.assertRaises(Exception): compile.compile_java_class(12)
        #compile.compile_java_class("Calculator.java")
        #compile.compile_java_test("CalculatorTest.java")
        #result = compile.run_tests("Calculator.java","CalculatorTest.java")
    
        #self.assertTrue(compile.is_passing(result))
        
if __name__ == '__main__':
    unittest.main()