import unittest
# from pegpy.tpeg import STDLOG

# def exTest(self, grammar, combinator):

#   parsers = {}
#   test = 0
#   ok = 0
#   logger = STDLOG

#   for i, testcase in enumerate(grammar['@@example']):
#     with self.subTest(i = i):
#         name, pos4 = testcase
#         if not name in grammar:
#             continue
#         if not name in parsers:
#             parsers[name] = combinator(grammar, start=name)
#         res = parsers[name](pos4.inputs, pos4.urn, pos4.spos, pos4.epos)
#         if res == 'err':
#             logger.perror(res.getpos4(), 'NG ' + name)
#             self.assertTrue(False)
#         else:
#             logger.println('OK', name, '=>', str(res))
#             self.assertTrue(True)
#   if test > 0:
#       logger.println('OK', ok, 'FAIL', test - ok, ok / test * 100.0, '%')


# unittest.TestCase.exTest = exTest
