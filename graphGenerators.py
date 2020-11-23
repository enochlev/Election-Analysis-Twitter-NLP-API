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
	"emotionsFile.txt",
	index_col=0,
	parse_dates=True,
	names=['ID','oldDate','Candidate','Sadness','Joy','Fear','Disgust','Anger'],
)
# Parse Date
df['Date'] = pd.to_datetime(df['oldDate'], format='%Y-%m-%d %H:%M:%S')

df['Date'] = df["Date"].apply( lambda df : datetime.datetime(year=df.year, month=df.month, day=df.day, hour=df.hour, minute=df.minute, second=df.second))
df.set_index(df["Date"],inplace=True)
del df["oldDate"]

#Split dataframe into 2 dataframes, one for each candidate.
biden = df.where(df['Candidate'] == 'Biden')
trump = df.where(df['Candidate'] == 'Trump')

### Emotions evoked by Joe Biden
plt.title(label="Emotions evoked by Joe Biden")
#plt.plot("Sadness", label="Sadness", data=biden.groupby([biden.index.minute]).mean())
plt.plot("Sadness", label="Sadness", data=biden.groupby([biden.index.day]).mean())
plt.plot("Joy", label="Joy", data=biden.groupby([biden.index.day]).mean())
plt.plot("Fear", label="Fear", data=biden.groupby([biden.index.day]).mean())
plt.plot("Disgust", label="Disgust", data=biden.groupby([biden.index.day]).mean())
plt.plot("Anger", label="Anger", data=biden.groupby([biden.index.day]).mean())
plt.savefig('results/emotions_evoked_by_joe_biden.png')

# ### Emotions evoked by Joe Biden
# plt.title(label="Emotions evoked by Donald Trump")
# plt.plot("Sadness", label="Sadness", data=trump.groupby([trump.index.day]).mean())
# plt.plot("Joy", label="Joy", data=trump.groupby([trump.index.day]).mean())
# plt.plot("Fear", label="Fear", data=trump.groupby([trump.index.day]).mean())
# plt.plot("Disgust", label="Disgust", data=trump.groupby([trump.index.day]).mean())
# plt.plot("Anger", label="Anger", data=trump.groupby([trump.index.day]).mean())
# plt.savefig('results/emotions_evoked_by_donald_trump.png')

### Emotions evoked by either presidential candidate
# plt.title(label="Emotions evoked by either presidential candidate")
# plt.plot("Sadness", label="Sadness", data=df.groupby([df.index.day]).mean())
# plt.plot("Joy", label="Joy", data=df.groupby([df.index.day]).mean())
# plt.plot("Fear", label="Fear", data=df.groupby([df.index.day]).mean())
# plt.plot("Disgust", label="Disgust", data=df.groupby([df.index.day]).mean())
# plt.plot("Anger", label="Anger", data=df.groupby([df.index.day]).mean())
# plt.savefig('results/emotions_evoked_by_either_candidate.png')

plt.legend(loc='upper left', bbox_to_anchor=(1.01, 1),
              ncol=1, borderaxespad=0)
plt.xlabel(xlabel="Day of November")
plt.axvline(x=2, label="Election Day", ls='--')

# display(df.groupby([df.index.day]).mean())

### Updating labels (not finished)
# xlabels = []

# for x in df['Date'].groupby([df.index.day]):
# 	xlabels.append(x['Date'].strftime('%m/%d'))
# 	print(x['Date'].strftime('%m/%d'))
leg = interactive_legend()
plt.show()

