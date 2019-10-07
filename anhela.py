# import IPython
import bpy
import nodeitems_builtins
from bpy.types import NodeTree, Node, NodeSocket, NodeSocketString, NodeReroute
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

def find_reroute_origin(link):
    print('find node reroute', link)

class AnhelaNodeTree(NodeTree):
    bl_label = "Anhela Node Tree"
    bl_icon = "NODETREE"

    def update(self):
        print('Full node tree update')

class AnhelaStringSocket(NodeSocket):
    bl_label = 'Anehla string socket'

    def text_update(self, context):
        print('text_update', self, context)

    text:bpy.props.StringProperty(
        name='String',
        default='socket to me',
        update=text_update
    )


    def draw_color(self, context, node):
        return (1.0, 0.0, 0.0, 0.7)

    def update(self):
        print('String socket update')

    def draw(self, context, layout, node, text):
        # print('drawing a socket with', self, context, layout, node, text)

        if self.is_output or self.is_linked:
            # layout.label(text=text)
            layout.label(text=self.text)
            # layout.label(text='out or linked')
        else:
            layout.prop(self, 'text')
            # layout.label(text='in and loose')

class AnhelaNode:
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == "AnhelaNodeTree"

class AnhelaNoteNode(Node, AnhelaNode):
    bl_label = "Note Node"
    bl_icon = 'TEXT'

class AnhelaCharacterNode(Node, AnhelaNode):
    bl_label = "Character Node"
    bl_icon = 'OUTLINER_DATA_ARMATURE'

    def name_update(self, context):
        print('name update', self, self.outputs)

    character_name: bpy.props.StringProperty(name='Name', default='MOTOKO', update=name_update)

    def init(self, context):
        name_output = self.outputs.new('AnhelaStringSocket', 'Name', identifier='name')
        print('init', self.outputs)

        print('init', self.outputs['Name'])

        # IPython.embed()
        # name_output.value_property = 'character_name'

    def update(self):
        print('Char node update')
        try:
            out = self.outputs['Name']
            print(
                'Update name from name!',
                out.is_linked and 'linked'
            )
            if out.is_linked:
                for o in out.links:
                    if o.is_valid:
                        print(
                            o.to_socket,
                            o.to_socket.name,
                            o.to_socket.node,
                        )

                        if isinstance(o.to_socket.node, NodeReroute):
                            print('rerouted, so??')

                        else:
                            o.to_socket.node.inputs[o.to_socket.name].text = self.character_name


                    else:
                        print('link', o, 'is invalid')
                        print(' --- ', o.to_socket.name)
                        print(' --- ', o.to_socket.node)

        except Exception as e: 
            print('something off with output node', e)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'character_name')


class AnhelaSceneNode(Node, AnhelaNode):
    bl_label = "Scene Node"
    bl_icon = 'OUTLINER_DATA_ARMATURE'

    time_specifier = [
        ("DAY", "DAY", "", 0),
        ("NIGHT", "NIGHT", "", 1)
    ]

    location_specifier = [
        ("INT", "INT.", "", 0),
        ("EXT", "EXT.", "", 1),
        ("INTEXT", "INT./EXT.", "", 1)
    ]

    day_or_night: bpy.props.EnumProperty(
        name="Time",
        description="XX",
        items=time_specifier,
        default='DAY',
    )

    int_or_ext: bpy.props.EnumProperty(
        name="Location",
        description="YY",
        items=location_specifier,
        default='INT',
    )

    def init(self, context):
        print('Scene node init')
        hero_input = self.inputs.new('AnhelaStringSocket', 'Hero')
        hero_output = self.outputs.new('AnhelaStringSocket', 'Hero')

    def update(self):
        print('Scene node update', self)

    def insert_link(self, link):
    
        if isinstance(link.from_node, NodeReroute):
            print('node reroute! so?')
            return

        print('Scene link', self, link, link.from_node, link.from_socket,
        '>>>', link.from_socket.text, '<<<'
        )

    def copy(self, node):
        print('Scene copy', self, node)

    def free(self):
        print('Scene free', self)

    def draw_buttons(self, context, layout):
        # print('Scene draw buttons', self, context, layout)
        layout.prop(self, 'int_or_ext')
        layout.prop(self, 'day_or_night')

    def draw_buttons_ext(self, context, layout):
        # print('Scene draw buttons ext', self, context, layout)
        pass

    def draw_label(self):
        # print('Scene label')

        return '{} - {}'.format(self.int_or_ext, self.day_or_night)

class AnhelaNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'AnhelaNodeTree'

node_categories = [
    AnhelaNodeCategory(
        'GENERIC',
        "Basic",
        items=[
            NodeItem('AnhelaCharacterNode'),
            NodeItem('AnhelaSceneNode')
        ]
    ),
    AnhelaNodeCategory(
        'LAYOUT',
        "Layout",
        items=[
            NodeItem('AnhelaNoteNode'),
            NodeItem("NodeFrame"),
            NodeItem("NodeReroute"),
        ]
    )
]

classes = (
    AnhelaNodeTree,
    AnhelaStringSocket,
    AnhelaNoteNode,
    AnhelaCharacterNode,
    AnhelaSceneNode
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    nodeitems_utils.register_node_categories('ANHELA_NODES', node_categories)

def unregister():
    nodeitems_utils.unregister_node_categories('ANHELA_NODES')

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    try:
        nodeitems_utils.unregister_node_categories('ANHELA_NODES')
    except:
        print('Keine Panik auf der Titanic')

    register()
