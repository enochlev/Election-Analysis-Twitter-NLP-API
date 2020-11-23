import matplotlib.pyplot as plt
import csv
import datetime
import string
import pandas as pd
from IPython.display import display
import numpy as np





class InteractiveLegend(object):
    def __init__(self, legend):
        self.legend = legend
        self.fig = legend.axes.figure

        self.lookup_artist, self.lookup_handle = self._build_lookups(legend)
        self._setup_connections()

        self.update()

    def _setup_connections(self):
        for artist in self.legend.texts + self.legend.legendHandles:
            artist.set_picker(10) # 10 points tolerance

        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)

    def _build_lookups(self, legend):
        labels = [t.get_text() for t in legend.texts]
        handles = legend.legendHandles
        label2handle = dict(zip(labels, handles))
        handle2text = dict(zip(handles, legend.texts))

        lookup_artist = {}
        lookup_handle = {}
        for artist in legend.axes.get_children():
            if artist.get_label() in labels:
                handle = label2handle[artist.get_label()]
                lookup_handle[artist] = handle
                lookup_artist[handle] = artist
                lookup_artist[handle2text[handle]] = artist

        lookup_handle.update(zip(handles, handles))
        lookup_handle.update(zip(legend.texts, handles))

        return lookup_artist, lookup_handle

    def on_pick(self, event):
        handle = event.artist
        if handle in self.lookup_artist:

            artist = self.lookup_artist[handle]
            artist.set_visible(not artist.get_visible())
            self.update()

    def on_click(self, event):
        if event.button == 3:
            visible = False
        elif event.button == 2:
            visible = True
        else:
            return

        for artist in self.lookup_artist.values():
            artist.set_visible(visible)
        self.update()

    def update(self):
        for artist in self.lookup_artist.values():
            handle = self.lookup_handle[artist]
            if artist.get_visible():
                handle.set_visible(True)
            else:
                handle.set_visible(False)
        self.fig.canvas.draw()

    def show(self):
        plt.show()


def interactive_legend(ax=None):
    if ax is None:
        ax = plt.gca()
    if ax.legend_ is None:
        ax.legend()

    return InteractiveLegend(ax.get_legend())


# Read CSV file
df = pd.read_csv(
	"Quartile\Overal_Quartile.csv",
    header=1,
	index_col=0,
	#parse_dates=True,
	names=['date','SQ2','SQ1','SQ3','JQ2','JQ1','JQ3','FQ2','FQ1','FQ3','DQ2','DQ1','DQ3','AQ2','AQ1','AQ3'],
)

trump = pd.read_csv(
	"Quartile\Trump_Quartiles.csv",
    header=1,
	index_col=0,
	#parse_dates=True,
	names=['date','SQ2','SQ1','SQ3','JQ2','JQ1','JQ3','FQ2','FQ1','FQ3','DQ2','DQ1','DQ3','AQ2','AQ1','AQ3'],
)

biden = pd.read_csv(
	"Quartile\Overal_Quartile.csv",
    header=1,
	index_col=0,
	#parse_dates=True,
	names=['date','SQ2','SQ1','SQ3','JQ2','JQ1','JQ3','FQ2','FQ1','FQ3','DQ2','DQ1','DQ3','AQ2','AQ1','AQ3'],
)

choice = int(input("1)trump\n2)biden\n3)both\n"))

if choice == 2:
    plt.title(label="Emotions evoked by Biden")
    plt.plot("SQ2","b", label="sadness_50th", data=biden)
    plt.plot("SQ1","b:", label="sadness_25th", data=biden)
    plt.plot("SQ3","b:", label="sadness_75th", data=biden)
    plt.plot("JQ2","y", label="joy_50th", data=biden)
    plt.plot("JQ1","y:", label="joy_25th", data=biden)
    plt.plot("JQ3","y:", label="joy_75th", data=biden)
    plt.plot("FQ2","k", label="fear_50th", data=biden)
    plt.plot("FQ1","k:", label="fear_25th", data=biden)
    plt.plot("FQ3","k:", label="fear_75th", data=biden)
    plt.plot("DQ2","g", label="disgust_50th", data=biden)
    plt.plot("DQ1","g:", label="disgust_25th", data=biden)
    plt.plot("DQ3","g:", label="disgust_75th", data=biden)
    plt.plot("AQ2","r", label="anger_50th", data=biden)
    plt.plot("AQ1","r:", label="anger_25th", data=biden)
    plt.plot("AQ3","r:", label="anger_75th", data=biden)
#plt.plot("Joy", label="joy", data=biden)
#plt.plot("Fear", label="Fear", data=biden.groupby([biden.index.day]).mean())
#plt.plot("Disgust", label="Disgust", data=biden.groupby([biden.index.day]).mean())
#plt.plot("Anger", label="Anger", data=biden.groupby([biden.index.day]).mean())
    plt.savefig('Quartile/emotions_evoked_by_joe_biden.png')
elif choice == 1:
# ### Emotions evoked by Joe Biden
    plt.title(label="Emotions evoked by  Trump")
    plt.plot("SQ2","b", label="sadness_50th", data=trump)
    plt.plot("SQ1","b:", label="sadness_25th", data=trump)
    plt.plot("SQ3","b:", label="sadness_75th", data=trump)
    plt.plot("JQ2","y", label="joy_50th", data=trump)
    plt.plot("JQ1","y:", label="joy_25th", data=trump)
    plt.plot("JQ3","y:", label="joy_75th", data=trump)
    plt.plot("FQ2","k", label="fear_50th", data=trump)
    plt.plot("FQ1","k:", label="fear_25th", data=trump)
    plt.plot("FQ3","k:", label="fear_75th", data=trump)
    plt.plot("DQ2","g", label="disgust_50th", data=trump)
    plt.plot("DQ1","g:", label="disgust_25th", data=trump)
    plt.plot("DQ3","g:", label="disgust_75th", data=trump)
    plt.plot("AQ2","r", label="anger_50th", data=trump)
    plt.plot("AQ1","r:", label="anger_25th", data=trump)
    plt.plot("AQ3","r:", label="anger_75th", data=trump)
    plt.savefig('Quartile/emotions_evoked_by_donald_trump.png')

### Emotions evoked by either presidential candidate
else:
# ### Emotions evoked by all
    plt.title(label="Emotions evoked by either Presidential Candidates")
    plt.plot("SQ2","b", label="sadness_50th", data=df)
    plt.plot("SQ1","b:", label="sadness_25th", data=df)
    plt.plot("SQ3","b:", label="sadness_75th", data=df)
    plt.plot("JQ2","y", label="joy_50th", data=df)
    plt.plot("JQ1","y:", label="joy_25th", data=df)
    plt.plot("JQ3","y:", label="joy_75th", data=df)
    plt.plot("FQ2","k", label="fear_50th", data=df)
    plt.plot("FQ1","k:", label="fear_25th", data=df)
    plt.plot("FQ3","k:", label="fear_75th", data=df)
    plt.plot("DQ2","g", label="disgust_50th", data=df)
    plt.plot("DQ1","g:", label="disgust_25th", data=df)
    plt.plot("DQ3","g:", label="disgust_75th", data=df)
    plt.plot("AQ2","r", label="anger_50th", data=df)
    plt.plot("AQ1","r:", label="anger_25th", data=df)
    plt.plot("AQ3","r:", label="anger_75th", data=df)
    plt.savefig('Quartile/emotions_evoked_by_Both_Candidates.png')
    

plt.legend(loc='upper left', bbox_to_anchor=(1.01, 1),
              ncol=1, borderaxespad=0)
plt.xlabel(xlabel="Day of November")
plt.axvline(x=2, label="Election Day", ls='--')
plt.axvline(x=3, label="End of Election Day", ls='--')
plt.axvline(x=6, label="Joe Biden Calld", ls='--')

# display(df.groupby([df.index.day]).mean())

### Updating labels (not finished)
# xlabels = []

# for x in df['Date'].groupby([df.index.day]):
# 	xlabels.append(x['Date'].strftime('%m/%d'))
# 	print(x['Date'].strftime('%m/%d'))
leg = interactive_legend()
plt.show()




