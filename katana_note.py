from Katana import NodegraphAPI
from Katana import KatanaFile
from Katana import PyXmlIO
from Katana import Nodes3DAPI

#获取节点————————————————————————————————————————————————————————————————————————————————————————————————————————————
def api_test():
    
    api_m=NodegraphAPI
    
    print(api_m)
    
    knode=NodegraphAPI.GetAllNodes(includeDeleted=False)    #获取所有节点  ,includeDeleted=False  被删除的节点是否计算
    
    for i in knode:
        print(i,i.getName(),i.getType())     #获取名字和类型


#获取指定节点——————————————————————————————————————————————————————————————————————————————————————————————
def getnode():

    typeNode=NodegraphAPI.GetAllNodesByType("Alembic_In",includeDeleted=False)      #获取所有Alembic_In类型的节点
    
    print(typeNode[0].getName())
    
    aa=NodegraphAPI.GetNode('Alembic_In')    #获取名字为Alembic_In的节点
    
    print(aa.getName())


#获取选择的节点————————————————————————————————————————————————————————————————————————————————
def catana_select():
    
    sel_list = NodegraphAPI.GetAllSelectedNodes()  #获取选择的节点
    
    for i in sel_list:
        
        print(i.getType,i.getName)

#获取当前的显示节点——————————————————————————————————————————————————————————————————————————————————————
def get_view():

    view = NodegraphAPI.GetViewNodes()      #获取当前的显示节点（ctrl+shift可以多个显示）

    print(view)


#获取根节点————————————————————————————————————————————————————————————————————————————————
def get_root():                            #这个方法用于获取所有的节点

    root = NodegraphAPI.GetRootNode()      #获取根节点
    
    print(root)
    
    children = root.getChildren()          #获取根节点下的所以子节点
    
    print(children)

#abc操作————————————————————————————————————————————————————————————————————————————————————————
def createAbc():

    knodes = NodegraphAPI.GetAllSelectedNodes()   #获取所以选择的节点
    
    root_node = NodegraphAPI.GetRootNode()        #获取根节点

    abc = NodegraphAPI.CreateNode("Alembic_In", parent=root_node)   #创建一个Alembic_In类型的节点

    abc.setName("abc1")                                             #设置节点的名字

    get_param = abc.getParameter("name")                            #获取节点的参数的name信息

    aa = get_param.getValue(0)                                      #获取name信息的参数

    print(aa)

    get_param.setUseNodeDefault(False)   #因为节点右边的有个默认参数按钮，所以一个参数栏有两个参数，这个语句是设置为非默认参数

    get_param.setValue("/root",1.0)      #设置数值

    get_param.getXML()                   #以xml的格式获取参数

    NodegraphAPI.SetNodePosition(abc,[300,0])     #设置节点在窗口的位置


#创建物体————————————————————————————————————————————————————————————————————————————————————————————————————————
def createPlan():

    root_node = NodegraphAPI.GetRootNode()

    plan = NodegraphAPI.CreateNode("PrimitiveCreate", parent=root_node)

    plan.setName("plane")

    NodegraphAPI.SetNodePosition(plan,[300,0])
    
    get_param = plan.getParameter("name")

    get_param.setValue("/root/world/set",1.0)

    get_param.setUseNodeDefault(False)
    
    type_param = plan.getParameter("type")

    type_param.setValue("poly plane",1.0)

    type_param.setUseNodeDefault(False)
    
    scale_param = plan.getParameter("transform.scale")       #获取数值

    scale_param.getChild("x").setValue(10,1.0)               #设置数值

    scale_param.getChild("x").setUseNodeDefault(False)       #非默认参数

    root_node = NodegraphAPI.GetRootNode()

    merge = NodegraphAPI.CreateNode("Merge", parent=root_node)

    NodegraphAPI.SetNodePosition(merge,[300,-30])

    input1 = merge.addInputPort("plane")                    #设置一个输入端口

    input1.connect(plan.getOutputPort("out"))               #设置输入端口连接的节点


#设置参数——————————————————————————————————————————————————————————————————————————————————————————————————————————
def get_value():

	knodes = NodegraphAPI.GetAllSelectedNodes() #获取所有的选择节点

	knode = knodes[0]

	param = knode.getParameters()      #获取第一个节点的所有参数

	print(param.getXML())

	children = param.getChildren()     #获取第一个节点的所有的子参数

	print(len(children))

	for i in children:                       

		print(i.getName(),i.getType())

		if i.getType()=="group":

		    for j in i.getChildren():   #子参数下的子参数
		        pass

		        print(j.getFullName(), j.getName())

	strck = children

	while strck:

		parameter = strck.pop()

		if not parameter.getChildren():    #如果这个子参数下没有子参数

			parm_type = parameter.getType()

        	if "Array"in parm_type:      #防止参数中有隐藏参数如 meger节点参数带有（add）类型=array

           		continue

		    print(parameter.getFullName(), parameter.getValue(1.0))

		    continue

		print(len(parameter.getChildren()))

		strck.extend(parameter.getChildren())


#属性的操作————————————————————————————————————————————————————————————————————————————————————————
def attr():

	knodes = NodegraphAPI.GetAllSelectedNodes()

	knode = knodes[0]

	attributes = knode.getAttributes()   #获取节点的属性信息

	print(attributes)

	attributes["x"]=0
	attributes["y"]=0

	knode.setAttributes(attributes)      #设置节点的属性信息

	knode.setBypassed(True)              #设置为pass

	knode.flushAll()                     #刷新节点

	knode.delete()                       #删除节点

	knode.setLocked(False)               #锁定节点


#场景信息查看——————————————————————————————————————————————————————————————————————————————————————
def get_scene_info():

	nodetypes=NodegraphAPI.GetNodeTypes()  #获取所以的节点类型

	print(NodegraphAPI.GetSourceFile())

	print(NodegraphAPI.GetProjectFile())

	print(NodegraphAPI.GetProjectDir())

	print(NodegraphAPI.GetKatanaSceneName())


#新建，导入，保存，导出————————————————————————————————————————————————————————————————————————————————
def new_load_save():

	KatanaFile.New()     #新建

	file_name = "/mnt/work/projects/nyj/asset/chr/test_chr_auto_pu/srf/task/katana/test_chr_auto_pu.srf.surfacing.v005.katana"

	KatanaFile.Load(file_name , isCrashFile=True)   #导入

	fileNameOrAssetId = "/mnt/work/projects/nyj/asset/chr/test_chr_auto_pu/srf/task/katana/test_chr_auto_pu.srf.surfacing.v005.katana"

	KatanaFile.Save(fileNameOrAssetId, extraOptionsDict=None)   #保存

	knodes =NodegraphAPI.GetAllSelectedNodes()

	NodegraphAPI.GetProjectFile()

	katana_scene = "/home/zejie/Desktop/test.katana"

	KatanaFile.Export(katana_scene, knodes, extraOptionsDict=None)      #导出

	KatanaFile.Import(katana_scene, floatNodes=False, parentNode=None)  #导入


#导出look_file————————————————————————————————————————————————————————————————————————
def look_file_bake():

	knode = NodegraphAPI.GetNode('LookFileBake')

	klf_file = "/mnt/work/projects/nyj/asset/chr/test_chr_auto_pu/srf/task/katana/test_chr_auto_pu.srf.surfacing.klf"

	klf_file_com = "/mnt/work/projects/nyj/asset/chr/test_chr_auto_pu/srf/task/katana/test_chr_auto_pu.srf.surfacing_com.klf"

	klf_file_asset = "/mnt/work/projects/nyj/asset/chr/test_chr_auto_pu/srf/task/katana/test_chr_auto_pu.srf.surfacing_asset.klf"

	klf_file_dri = "/mnt/work/projects/nyj/asset/chr/test_chr_auto_pu/srf/task/katana/test_chr_auto_pu.srf.surfacing_dir.klf"

	knode.WriteToLookFile(None, klf_file)#正常的打包文件

	knode.WriteToCompoundFile(None, klf_file_com, includeGlobalAttributes=True, includeLodInfo=True)#打包文件并把所有的passes都打包

	knode.WriteToAsset(None, klf_file_asset) #打包文件并把所有的passes和属性都打包，这个是最高级别的打包文件

	knode.WriteToDirectory(None, klf_file_dri, includeGlobalAttributes=True, includeLodInfo=True)#只把数据导出来，不打包文件，这个是最低级别的打包文件


#导出xml文件————————————————————————————————————————————————————————————————————————
def export_xml():

	knodes = NodegraphAPI.GetAllSelectedNodes()

	xml = NodegraphAPI.BuildNodesXmlIO(knodes)    #创建xml输入输出

	print(xml.writeString())     #把节点转换为xml格式的字符

	xml_file = "/home/zejie/Desktop/test.xml"

	xml.write(xml_file)        #导出xml文件格式


#导入xml文件————————————————————————————————————————————————————————————
def import_xml():

	from Katana import PyXmlIO

	xml_scene = "/home/zejie/Desktop/test.xml"
	
	#方法一
	element, upgraded = NodegraphAPI.LoadElementsFromFile(xml_scene, versionUp=True)   #导入xml文件
	print(element.writeString()) 
	xml_string = NodegraphAPI.LoadXmlFromFile(xml_scene)   #以字符串的形式导入文件
	print(xml_string)

	#方法二
	parser = PyXmlIO.Parser()       #创建解析器
	xml = parser.parse(xml_scene)   #解析xml文件
	xml_element = xml.writeString()
	element, upgraded = NodegraphAPI.LoadElementsFromString(xml_element, versionUp=True)   #导入xml文件
	print(element)

	parent = NodegraphAPI.GetRootNode()   #获取根节点
	KatanaFile.Paste(element, parent)     #把xml文件转换为节点，放到根目录下


#组的操作————————————————————————————————————————
def group_():

	parent = NodegraphAPI.GetRootNode()

	kgroup = NodegraphAPI.GetNode('Group')

	#kgroup = NodegraphAPI.CreateNode("Group", parent=parent)    #创建组

	knodes = NodegraphAPI.GetAllSelectedNodes()

	for n in knodes:
		
		n.setParent(kgroup)                                      #把选择的物体放到组里

	path = "/home/zejie/Desktop/test.livegroup"

	live_group = NodegraphAPI.ConvertGroupToLiveGroup(kgroup)    #把普通组转换为livegroup

	live_group.makeEditable(includingAllParents=False)           #设置组内可编辑

	live_group.publishAssetAndFinishEditingContents(filenameOrAssetID=path)   #设置储存路径，并保存

	live_group.coconvertToGroup()      #livegroup转换为普通组


#设置全局变量————————————————————————————————————————————————————————————
def global_variables():

	root_node = NodegraphAPI.GetRootNode()

	variable_paramete = root_node.getParameter('variables')  #获取全局变量

	label = "camera1"

	values = ["alembic","default","default1","default2"]
	 
	#获取现在有的全局变量
	exists_variables =[]
	for child in variable_paramete.getChildren():
		print(child.getName())
		exists_variables.append(child.getName())

	#如果已有的全局变量和需要添加的全局变量有冲突。删除已有的全局变量
	if label in exists_variables:
		exists_variables = variable_paramete.getChild(label)
		variable_paramete.deleteChild(exists_variables)
	 
	child_group = variable_paramete.createChildGroup(label) #创建一个全局变量
	child_group.createChildNumber("enable",1)               #设置变量可见

	children = child_group.createChildStringArray("options",len(values),1) #为变量的值创建一个数组

	for index,child in enumerate(children.getChildren()):
		#print(child.getName())
		child_group.createChildString("value",values[index])    #数组变量的每个值定义一个字符串类型的值
		child.setValue(values[index], 1)   #赋值个数组的每个值

	#print(variable.getXML())

def global_variables_2():

    root_node = NodegraphAPI.GetRootNode()

    variable_paramete = root_node.getParameter('variables')

    label = "camera1"

    values = ["alembic","default","default1","default2"]

    variable = variable_paramete.createChildString(label,"") #创建一个全局变量

    hint ={"widget":"popup" ,"options":values}

    variable.setHintString(str(hint))

    variable.ssetValue(values[0],1)

#创建tx文件    ././maketx  ././xxx.jpj  ././xxx.tx


#获取大纲的模型————————————————————————————————————————————————————————————————————————
from Katana import Nodes3DAPI

def getGeometryProducer():

	knode = NodegraphAPI.GetNode('Outdoor_Dawn__Render_n20010')

	NodegraphAPI.SetNodeViewed(knode, True, exclusive=True)     #设置为这个节点显示

	producer = Nodes3DAPI.GetGeometryProducer(node=knode, graphState=None, portIndex=0)     #获取几何体类 放回   /root  

	location =  '/root/world/geo/assets/chr/test_chr_auto_pu/master/poly/hi/geometry/mesh_grp/skin_grp/body_geo'

	if location:

		current_producer = producer.getProducerByPath(location)   #根据路径获取路径下的几何体
	else:
		current_producer = producer
		
	stack = [current_producer]

	while stack:    #第归遍历

		child =stack.pop()

		children = child.iterChildren()    #获取所有子资产

		print(child.getFullName())

		stack.extend(children)


#获取物体属性——————————————————————————————————————————————————————————————————
def getGeometryAttr():

	from Katana import Nodes3DAPI

	knode = NodegraphAPI.GetNode('Outdoor_Dawn__Render_n20010')

	NodegraphAPI.SetNodeViewed(knode, True, exclusive=True)

	producer = Nodes3DAPI.GetGeometryProducer(node=knode, graphState=None, portIndex=0)     #/root

	location = '/root/world/geo/assets/chr/test_chr_auto_pu/master/poly/hi/geometry/mesh_grp/skin_grp/body_geo/polysurface2/polysurface2Shape'

	current_producer = producer.getProducerByPath(location)

	attributes = current_producer.getAttributeNames() 

	print(attributes)

	scenegraph_attr = current_producer.getDelimitedGlobalAttribute("geometry.arbitrary.st.scope")  #获取某个属性的单个值

	print(scenegraph_attr.getValue())

	global_attr = current_producer.getGlobalAttribute("geometry")  #获取某个属性的全部值

	print(global_attr.getData())

	print(global_attr.getXML())


#创建一个shelf——————————————————————————————————————————————————————————————————————————————————————
def create_shelf():
	from Katana import Shelves

	name = "test"

	shelf = Shelves.Shelf(name,"/home/zejie/.katana/Shelves/guanzejie/",Shelves.SHELF_TYPE_USER)   #获取一个shelf

	item = shelf.find(name)   #查看一个已有的shelf

	#item.run(True)           #执行一个item

	#print item.getName()     #获取一个item名字

	#print item.getIconName() #获取一个item的icon

	#print item.getSourceFile()  #获取一个item的文件路径

	#item.deleteSourceFile()     #删除一个item

	temp = shelf.createItem(name, "discription", icon=None)    #创建一个item

	scope = "print('hello guanzejie')"

	temp.setScope(scope)   #设置item的代码

	print(temp.getScope())

	Shelves.CreateUserShelf("haha")   #创建一个shelf

	shelf_name = Shelves.GetUserShelves()   #获取自己创建的shelf

	for i in shelf_name:

	    print(i.getName())


#获取ui——————————————————————————————————————————————
def getUi():

	from PyQt5 import QtWidgets
	import UI4       #这是个用qt包装的类

	for widget in QtWidgets.qApp.topLevelWidgets():   #获取主窗口的全部主组件
	    if widget.objectName() == "mainWindow":       #获取主窗口组件
		#print(widget.objectName())
		#print(widget)
		main_window = widget

	print(UI4.App.Layouts._PrimaryWindow)
	main_window = UI4.App.Layouts._PrimaryWindow      #获取主窗口组件

	for each in main_window.children():                #获取主窗口的子组件
	    #print(each.objectName(),each)
	    pass

	main_menu = main_window.findChild(UI4.App.MainMenu.MainMenu)      #获取菜单栏

	for each in main_menu.children():
	    #print(each.objectName(),each)
	    pass

	for each in main_window.children():

	    print(each,each.objectName())

	    if layout.objectName() == "mainLayout":    #获取窗口的布局

		#print(layout)
		pass

#菜单栏创建按钮————————————————————————————————————————————————————————————————————————————————————————

from PyQt5 import QtWidgets
import UI4

def connect_def():
	
	print("aaaaaaaaaa")

def createButton():

	for widget in QtWidgets.qApp.topLevelWidgets():    #获取主窗口的全部主组件
	    if widget.objectName() == "mainWindow":        #获取主窗口

		main_window = widget
	 
	main_menu = main_window.findChild(UI4.App.MainMenu.MainMenu)    #获取主菜单窗口

	menu = QtWidgets.QMenu(parent = main_menu)     #创建新按钮

	menu.setTitle("publish")                       #设置按钮的名字

	for i in main_menu.findChildren(QtWidgets.QMenu):   #获取窗口的子组件
	    if i.title() == "publish":  #获取组件名字
		pass
		i.deleteLater()   #删除组件
	    #print(i.title())

	main_menu.addMenu(menu)      #添加按钮到菜单上

	tools = ["aaaaa","bbbbb","ccccc","ddddd"]

	for tool in tools:
	    action = QtWidgets.QAction(menu)  #定义下拉按钮
	    action.setText(tool)              #设置按钮的名字
	    action.triggered.connect(connect_def)          #创建连接
	    menu.addAction(action)            #添加到下拉按钮

	menu2 = QtWidgets.QMenu(parent = main_menu)
	menu2.setTitle("save")

	menu.addMenu(menu2)

	for tool in tools:
	    action = QtWidgets.QAction(menu2)
	    action.setText(tool)
	    menu2.addAction(action)


#创建菜单栏和创建窗口菜单——————————————————————————————————————————————————————————————
from PyQt5 import QtWidgets
import UI4

def connect_def():

    print("hahahahaha")

def creatWindowButton():
	main_window = UI4.App.Layouts._PrimaryWindow

	main_menu = main_window.findChild(UI4.App.MainMenu.MainMenu)

	main_layout = main_window.findChildren(QtWidgets.QLayout)     #获取布局

	for lay in main_layout:

	    if lay.objectName()=="mainMenuLayout":

		layout_ = lay

	print(layout_.objectName())

	toolbar =QtWidgets.QToolBar(parent = main_menu)    #设置一个新的窗口布局

	toolbar.setObjectName("aaaaa")
	toolbar.setWindowTitle("title")

	layout_.addWidget(toolbar)         #把布局添加到窗口上

	for i in main_menu.findChildren(QtWidgets.QMenu):

	    if i.title() == "publish":
		pass
		i.deleteLater()

	menu = QtWidgets.QMenu(parent = main_menu)

	menu.setTitle("publish")

	#main_menu.addMenu(menu)

	action = QtWidgets.QAction(menu)

	action.setText("aa")

	action.triggered.connect(connect_def)

	menu.addAction(action)

	toolbar.addAction(action)    #窗口添加按钮

	#menu.deleteLater()



    





