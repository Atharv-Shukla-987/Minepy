from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

Player = FirstPersonController(position = (0,5,0),scale=(1,0.95,1))

application.asset_folder = Path('./Assets')

blocks = {
    'grass': {'texture': load_texture('grass'),'hand': load_texture('hgrass'), 'sound': 'sound/grass_mine'},
    'dirt':  {'texture': load_texture('dirt'), 'hand': load_texture('hdirt'), 'sound': 'sound/dirt_mine'},
    'stone': {'texture': load_texture('stone'), 'hand': load_texture('hstone'),'sound': 'sound/stone_mine'},
    'bedrock': {'texture': load_texture('bedrock'),'hand': load_texture('hbedrock'), 'sound': 'sound/bedrock_mine'},
}

occupied_positions = set()
mined_positions = set()
def gen_world(x,y,z,block):
   pos = (int(x),int(y),int(z))
   if pos not in occupied_positions and pos not in mined_positions :
       e =Entity(
        model='cube',
        scale=1,
        position = pos,
        texture= blocks[block]['texture'],
        collider='box'
       )
       e.is_block = True
       e.block = block                  
       occupied_positions.add(pos)

def update():
    Hand()
    pos_player = int(max(abs(Player.x),abs(Player.z)))
    for i in range(pos_player+5):
        y=-3
        gen_world(0,y,i ,'bedrock')
        gen_world(i,y,i,'bedrock')
        gen_world(i,y,0,'bedrock')
        gen_world(i,y,-i,'bedrock')
        gen_world(0,y,-i,'bedrock')
        gen_world(-i,y,i,'bedrock')
        gen_world(-i,y,-i,'bedrock')
        gen_world(-i,y,0,'bedrock')
       
        for x in range(i):
            gen_world(x,y,i,'bedrock')
            gen_world(i,y,x,'bedrock')
            gen_world(x,y,-i,'bedrock')
            gen_world(-i,y,x,'bedrock')
            gen_world(-x,y,i,'bedrock')
            gen_world(i,y,-x,'bedrock')
            gen_world(-x,y,-i,'bedrock')
            gen_world(-i,y,-x,'bedrock')
    for i in range(pos_player+5):
        y=-2
        gen_world(0,y,i ,'stone')
        gen_world(i,y,i,'stone')
        gen_world(i,y,0,'stone')
        gen_world(i,y,-i,'stone')
        gen_world(0,y,-i,'stone')
        gen_world(-i,y,i,'stone')
        gen_world(-i,y,-i,'stone')
        gen_world(-i,y,0,'stone')
       
        for x in range(i):
            gen_world(x,y,i,'stone')
            gen_world(i,y,x,'stone')
            gen_world(x,y,-i,'stone')
            gen_world(-i,y,x,'stone')
            gen_world(-x,y,i,'stone')
            gen_world(i,y,-x,'stone')
            gen_world(-x,y,-i,'stone')
            gen_world(-i,y,-x,'stone')

    for i in range(pos_player+5):
        y=-1
        gen_world(0,y,i,'dirt')
        gen_world(i,y,i,'dirt')
        gen_world(i,y,0,'dirt')
        gen_world(i,y,-i,'dirt')
        gen_world(0,y,-i,'dirt')
        gen_world(-i,y,i,'dirt')
        gen_world(-i,y,-i,'dirt')
        gen_world(-i,y,0,'dirt')
       
        for x in range(i):
            gen_world(x,y,i,'dirt')
            gen_world(i,y,x,'dirt')
            gen_world(x,y,-i,'dirt')
            gen_world(-i,y,x,'dirt')
            gen_world(-x,y,i,'dirt')
            gen_world(i,y,-x,'dirt')
            gen_world(-x,y,-i,'dirt')
            gen_world(-i,y,-x,'dirt')
    
    for i in range(pos_player+5):
        y=0
        gen_world(0,y,i,'grass')
        gen_world(i,y,i,'grass')
        gen_world(i,y,0,'grass')
        gen_world(i,y,-i,'grass')
        gen_world(0,y,-i,'grass')
        gen_world(-i,y,i,'grass')
        gen_world(-i,y,-i,'grass')
        gen_world(-i,y,0,'grass')
       
        for x in range(i):
            gen_world(x,y,i,'grass')
            gen_world(i,y,x,'grass')
            gen_world(x,y,-i,'grass')
            gen_world(-i,y,x,'grass')
            gen_world(-x,y,i,'grass')
            gen_world(i,y,-x,'grass')
            gen_world(-x,y,-i,'grass')
            gen_world(-i,y,-x,'grass')

inventory = {}
blk_in_inven = []
selblk = 0


slot1 = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.gray,
    position=(-0.225, 0.45),
    scale=0.05
)
slot2 = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.gray,
    position=(-0.175, 0.45),
    scale=0.05
)
slot3 = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.gray,
    position=( -0.125, 0.45),
    scale=0.05
)
slot4 = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.gray,
    position=(-0.075, 0.45),
    scale=0.05
)
slot5 = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.gray,
    position=(-0.025, 0.45),
    scale=0.05
)
slot6 = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.gray,
    position=(0.025, 0.45),
    scale=0.05
)
slot7 = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.gray,
    position=(0.075, 0.45),
    scale=0.05
)
slot8 = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.gray,
    position=(0.125, 0.45),
    scale=0.05
)
slot9 = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.gray,
    position=(0.175, 0.45),
    scale=0.05
)
slot10 = Entity(
    parent = camera.ui,
    model = 'quad',
    color=color.gray,
    position=(0.225, 0.45),
    scale=0.05
)

slots = [slot1,slot2,slot3,slot4,slot5,slot6,slot7,slot8,slot9,slot10]

hand = Entity(
    parent=camera.ui,
    model='quad',
    scale= 0.8,
    color = color.white,
    position=(0.6, -0.35, 1),
)

def Hand():
    if blk_in_inven:
        hand.texture = blocks[blk_in_inven[selblk]]['hand']
        hand.visible = True
        hand.color = color.white
    else:
        hand.visible = False
        hand.alpha = 0.0

        
def input(key):
    global selblk
    
    if key == 'scroll up' and len(blk_in_inven):
        selblk = (selblk + 1) % len(blk_in_inven)
    
    if key == 'scroll down' and len(blk_in_inven):
        selblk = (selblk - 1) % len(blk_in_inven)
        
    if key == 'left mouse down':
        entity =  mouse.hovered_entity
        entity = mouse.hovered_entity
        if entity and getattr(entity, 'is_block', False):
            pos = (int(entity.x), int(entity.y), int(entity.z))
            block = entity.block
            if block != 'bedrock' :
                occupied_positions.discard(pos)
                mined_positions.add(pos)
                destroy(entity)
                Audio(blocks[block]['sound'],1,autoplay=True)
                if block not in inventory:
                    blk_in_inven.append(block)
                    inventory[block] = 1
                else:
                    inventory[block] += 1
                for i, slot in enumerate(slots):
                    if i < len(blk_in_inven) : 
                        slot.texture = blocks[blk_in_inven[i]]['hand'] 
                    else:
                        None
    if key=='right mouse down' :
        if not blk_in_inven:
           return
        entity = mouse.hovered_entity
        if entity and getattr(entity , 'is_block', False):
            pos = int(entity.x + mouse.normal.x),int(entity.y + mouse.normal.y),int(entity.z + mouse.normal.z)
            if pos not in occupied_positions :
                e = Entity(
                    model='cube',
                    scale=1,
                    position = pos ,
                    texture=blocks[blk_in_inven[selblk]]['texture'],
                    collider='box'
                )
                e.is_block = True
                e.block = blk_in_inven[selblk]
                occupied_positions.add(pos)
                mined_positions.discard(pos)
                Audio(blocks[blk_in_inven[selblk]]['sound'] , 1 , autoplay=True)
                inventory[blk_in_inven[selblk]] -= 1
                if inventory[blk_in_inven[selblk]] == 0:
                    del inventory[blk_in_inven[selblk]]
                    blk_in_inven.pop(selblk)
                    slots[selblk].texture = None
                if blk_in_inven:
                    selblk = min(selblk, len(blk_in_inven) - 1)
                else:
                    selblk = 0
                for i, slot in enumerate(slots):
                    if i < len(blk_in_inven): 
                        slot.texture = blocks[blk_in_inven[i]]['hand'] 
                    else:
                        None
 
app.run()