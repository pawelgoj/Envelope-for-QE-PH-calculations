import tkinter as tk
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

data1 = {'Country': ['US','CA','GER','UK','FR'],
         'GDP_Per_Capita': [45000,42000,52000,49000,47000]
}
df1 = DataFrame(data1,columns=['Country','GDP_Per_Capita'])

 

root= tk.Tk() 
  
fig, ax = plt.subplots()
bar1 = FigureCanvasTkAgg(fig, root)

bar1.get_tk_widget().pack(side='left', fill='both')

df1 = df1[['Country','GDP_Per_Capita']].groupby('Country').sum()
df1.plot(kind='bar', legend=True, ax=ax)
ax.set_title('Country Vs. GDP Per Capita')

root.mainloop()