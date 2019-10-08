from bpy.props import StringProperty
from bpy.types import NodeTree, Node, NodeSocket, NodeSocketString, NodeReroute
from functools import reduce
from nodeitems_utils import NodeCategory, NodeItem
import bpy
import nodeitems_builtins
import nodeitems_utils

BNT = "Bnhela Node Tree"

bl_info = {
    'name': 'Bnhela Node Tree',
    'author': 'gabriel montagné, gabriel@tibas.london',
    'version': (0, 0, 1),
    'blender': (2, 80, 0),
    'description': 'Node tree for sketching scene relationships',
    'tracker_url': 'https://github.com/gabrielmontagne/blender-addon-bnhela/issues'
}

def collate(acc, socket):
    node = socket.node

    if node.bl_idname == 'NodeReroute':
        return reduce(collate, [l.to_socket for l in node.outputs[0].links], acc)

    return acc + [socket]

def get_all_outputs(socket):
    return reduce(collate, [l.to_socket for l in socket.links], [])

class BnhelaNodeTree(NodeTree):
    bl_label = BNT
    bl_icon = "EVENT_B"

class BnhelaEagerSocket():
    def on_name_update(self, context):

        if not self.is_output:
            return

        others = get_all_outputs(self)

        for other in others:
            if other.bl_idname != self.bl_idname:
                return

            other.payload = self.payload
            other.node.update()

    payload: StringProperty('Name', update=on_name_update, default='')

    def draw(self, context, layout, node, text):
        layout.label(text=self.name.lower() + ' ' + self.payload)

class BnhelaCharacterSocket(BnhelaEagerSocket, NodeSocket):

    bl_label = 'Bnhela Character Socket'

    def draw_color(self, context, node):
        return (0.6, 0.0, 0.0, 1.0)

class BnhelaLocationSocket(BnhelaEagerSocket, NodeSocket):

    bl_label = 'Bnhela Character Socket'

    def draw_color(self, context, node):
        return (0.6, 0.0, 0.6, 1.0)

class BnhelaNode:

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == BNT

class BnhelaLocationNode(Node, BnhelaNode):

    bl_label = "Location Node"
    bl_icon = 'VIEW_PERSPECTIVE'

    def on_payload_update(self, context):
        self.update()

    payload: StringProperty(update=on_payload_update)

    def draw_buttons(self, context, layout):
        layout = layout
        layout.prop(self, 'payload', text='Namε')

    def init(self, context):
        self.outputs.new('BnhelaLocationSocket', 'Name')

    def update(self):
        name_socket = self.outputs['Name']
        name_socket.payload = self.payload

    def draw_label(self):
        return '{} - λ'.format(self.payload)

class BnhelaCharacterNode(Node, BnhelaNode):

    bl_label = "Character Node"
    bl_icon = 'OUTLINER_DATA_ARMATURE'

    def on_payload_update(self, context):
        self.update()

    payload: StringProperty(update=on_payload_update)

    def draw_buttons(self, context, layout):
        layout = layout
        layout.prop(self, 'payload', text='Namε')

    def init(self, context):
        self.outputs.new('BnhelaCharacterSocket', 'Name')

    def update(self):
        name_socket = self.outputs['Name']
        name_socket.payload = self.payload

    def draw_label(self):
        return '{} - χ'.format(self.payload)

class BnhelaSceneNode(Node, BnhelaNode):

    bl_label = "Scene Node"
    bl_icon = 'VIEW_CAMERA'

    time_specifier = [
        ("DAY", "DAY", "", 0),
        ("NIGHT", "NIGHT", "", 1)
    ]

    day_or_night: bpy.props.EnumProperty(
        name="Time",
        items=time_specifier,
        default='DAY',
    )

    location_specifier = [
        ("INT.", "INT.", "", 0),
        ("EXT.", "EXT.", "", 1),
        ("INT./EXT.", "INT./EXT.", "", 2)
    ]

    int_or_ext: bpy.props.EnumProperty(
        name="Location",
        description="YY",
        items=location_specifier,
        default='INT.',
    )

    char_titles = [
        'MC',
        'OP',
        'WC'
    ]

    scene_index: bpy.props.IntProperty(name='Scene index', min=0)

    def init(self, context):
        self.width = 200

        self.inputs.new('BnhelaLocationSocket', 'Location')

        for char_title in self.char_titles:
            self.inputs.new('BnhelaCharacterSocket', char_title)
            self.outputs.new('BnhelaCharacterSocket', char_title)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'int_or_ext')
        layout.prop(self, 'day_or_night')
        layout.prop(self, 'scene_index')

    def draw_label(self):
        return '{:03d}. {} - {}'.format(self.scene_index, self.int_or_ext, self.day_or_night)

    def update(self):
        for char_title in self.char_titles:
            input = self.inputs[char_title]
            output = self.outputs[char_title]

            if not input.is_linked:
                input.payload = ''

            output.payload = input.payload

classes = (
    BnhelaNodeTree,
    BnhelaCharacterNode,
    BnhelaLocationNode,
    BnhelaSceneNode,
    BnhelaCharacterSocket,
    BnhelaLocationSocket,
)

class BnhelaNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'BnhelaNodeTree'

node_categories = [
    BnhelaNodeCategory(
        'GENERIC',
        "Basic",
        items=[
            NodeItem("BnhelaCharacterNode"),
            NodeItem("BnhelaLocationNode"),
            NodeItem("BnhelaSceneNode"),
        ]
    ),

    BnhelaNodeCategory(
        'LAYOUT',
        "Layout",
        items=[
            NodeItem("NodeFrame"),
            NodeItem("NodeReroute"),
        ]
    )
]

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    nodeitems_utils.register_node_categories('BNHELA_NODES', node_categories)

def unregister():
    nodeitems_utils.unregister_node_categories('BNHELA_NODES')

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    try:
        nodeitems_utils.unregister_node_categories('BNHELA_NODES')
    except:
        print('Keine Panik auf der Titanic')

    register()
