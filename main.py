import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
figure = make_subplots(cols=1,
                       rows=len(os.listdir('./dataFiles')),
                       subplot_titles=['Graph of {}.'.format(os.path.split(x)[1]) for x in os.listdir('./dataFiles')])
figure.update_layout(title='Profilometer graph{}'.format('s' if len(os.listdir('./dataFiles')) > 1 else ''),
                     showlegend=False)
for fileIndex, file in enumerate(os.scandir('./dataFiles')):
    with open(file, 'r') as fileObj:
        fileString = fileObj.read()
        fileDict = {}
        for lineIndex, line in enumerate(fileString.splitlines()):
            lineIndex += 1
            splitLine = line.split(':')
            if splitLine[0] == "SCALED DATA":
                break
            fileDict[splitLine[0].strip()] = splitLine[1].strip()
        readings = []
        for number in ''.join(fileString.splitlines()[lineIndex:-3]).split('\t'):
            if number == '':
                continue
            readings.append(float(number.strip()))
        figure['layout'][f'xaxis{fileIndex + 1}']['title'] = 'Lateral Distance (micron)'
        figure['layout'][f'yaxis{fileIndex + 1}']['title'] = 'Height (Å)'
        figure.append_trace(
            go.Scatter(
                x=[(x * float(fileDict['Sclen'])) / int(fileDict['NumPts']) for x in range(int(fileDict['NumPts']))],
                y=readings,
                mode='lines',
                name='Graph of {}.'.format(os.path.split(file)[1]),
            ),
            row=fileIndex+1,
            col=1
        )
figure.show()
figure.write_html('index.html')