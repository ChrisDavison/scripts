from prelude.timerange import *

# class TestTimeRange(unittest.TestCase):
#     import dateutil.parser
#     def testDays(self):
#         """Return an inclusive sequence of days."""
#         tr = TimeRange('2017-01-01', '2017-01-02')
#         expected = [dateutil.parser.parse('2017-01-01'),
#                     dateutil.parser.parse('2017-01-02')]
#         self.assertEqual(expected, list(tr.days()))

#     def testHours(self):
#         """Return an inclusive sequence of hours."""
#         tr = TimeRange('2017-01-01 00:00:00', '2017-01-01 08:00:00')
#         expected = [dateutil.parser.parse('2017-01-01 00:00:00'),
#                     dateutil.parser.parse('2017-01-01 01:00:00'),
#                     dateutil.parser.parse('2017-01-01 02:00:00'),
#                     dateutil.parser.parse('2017-01-01 03:00:00'),
#                     dateutil.parser.parse('2017-01-01 04:00:00'),
#                     dateutil.parser.parse('2017-01-01 05:00:00'),
#                     dateutil.parser.parse('2017-01-01 06:00:00'),
#                     dateutil.parser.parse('2017-01-01 07:00:00'),
#                     dateutil.parser.parse('2017-01-01 08:00:00')]
#         self.assertEqual(expected, list(tr.hours()))

#     def testSeconds(self):
#         """Return an inclusive sequence of seconds."""
#         tr = TimeRange('2017-01-01 00:00:00', '2017-01-01 00:00:05')
#         expected = [dateutil.parser.parse('2017-01-01 00:00:00'),
#                     dateutil.parser.parse('2017-01-01 00:00:01'),
#                     dateutil.parser.parse('2017-01-01 00:00:02'),
#                     dateutil.parser.parse('2017-01-01 00:00:03'),
#                     dateutil.parser.parse('2017-01-01 00:00:04'),
#                     dateutil.parser.parse('2017-01-01 00:00:05')]
#         self.assertEqual(expected, list(tr.seconds()))

#     def testMinutes(self):
#         """Return an inclusive sequence of minutes."""
#         tr = TimeRange('2017-01-01 00:00:00', '2017-01-01 00:03:00')
#         expected = [dateutil.parser.parse('2017-01-01 00:00:00'),
#                     dateutil.parser.parse('2017-01-01 00:01:00'),
#                     dateutil.parser.parse('2017-01-01 00:02:00'),
#                     dateutil.parser.parse('2017-01-01 00:03:00')]
#         self.assertEqual(expected, list(tr.minutes()))

#     def testGenerateStartAfterEnd(self):
#         """Allow backwards time traversal."""
#         tr = TimeRange('2017-01-02', '2017-01-01')
#         expected = [dateutil.parser.parse('2017-01-02'),
#                     dateutil.parser.parse('2017-01-01')]
#         self.assertEqual(expected, list(tr.days()))
