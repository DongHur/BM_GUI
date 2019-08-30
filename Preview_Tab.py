# from widgets.BP_Graph import BP_Graph

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

class Preview_Tab():
    def __init__(self, parent):
        self.test = "test"
        self.parent = parent
    def setup(self):
        # self.smallBPGraph = BP_Graph() # small body point graph
        # self.smallBPcanvas = FigureCanvas(self.smallBPGraph)
        # self.smallBPGraph.init_plot()
        # self.parent.Preview_Ant_Layout.addWidget(self.smallBPcanvas)

        # Append tSNE Graph
        self.tsneGraph = tsne_Graph()
        self.tsnecanvas = FigureCanvas(self.tsneGraph)
        self.tsneGraph.init_plot()
        self.horizontalLayout_3.addWidget(self.tsnecanvas)

        # Append Density Graph
        self.densityGraph = density_Graph() # total density graph
        self.densitycanvas = FigureCanvas(self.densityGraph)
        self.densityGraph.init_plot(title='Total Density Plot')
        self.totalBehaviorLayout.addWidget(self.densitycanvas)
        pass