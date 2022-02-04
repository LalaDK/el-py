from rich.progress import track
from rich import print
import plotext as plt

# os.system('cls' if os.name == 'nt' else 'clear')
#
# def to_d(x):
#     plt.datetime.set_datetime_form(date_form='%H:%M')
#     t = datetime.fromtimestamp(int(x.get('from_datetime')))
#     return plt.datetime.datetime_to_string(t)
#
#
# names = list(map(lambda x : to_d(x), arr))
# values = list(map(lambda x : x.get('kwh'), arr))
# plt.bar(names, values, width = 0.3)
# plt.grid(0, 1)
# plt.ylim(0, 4)
# plt.title("Strømforbrug")
# plt.clc() # to remove colors
# plt.xlabel("Tidspunkt")
# plt.ylabel("kWh")
# plt.show()
