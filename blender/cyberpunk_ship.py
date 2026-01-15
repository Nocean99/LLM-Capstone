import bpy
import math

# ============================================
# SETUP - Clear scene
# ============================================
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

for block in bpy.data.meshes:
    if block.users == 0:
        bpy.data.meshes.remove(block)
for block in bpy.data.materials:
    if block.users == 0:
        bpy.data.materials.remove(block)
for block in bpy.data.images:
    if block.users == 0:
        bpy.data.images.remove(block)

print("Importing mesh...")

# ============================================
# IMPORT THE GLB MODEL
# ============================================
bpy.ops.import_scene.gltf(
    filepath=r"C:\Users\noahs\Desktop\ai experiments\blender\Meshy_AI_A_highly_detailed_or_0112213335_generate.glb"
)

imported_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
if not imported_objects:
    imported_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']

bpy.ops.object.select_all(action='DESELECT')
for obj in imported_objects:
    obj.select_set(True)
bpy.context.view_layer.objects.active = imported_objects[0]

if len(imported_objects) > 1:
    bpy.ops.object.join()

ship = bpy.context.active_object
ship.name = "Spaceship"

bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

# Position ship smaller and in lower portion - hovering over planet
ship.location = (0, 0, -0.3)

max_dim = max(ship.dimensions)
if max_dim > 0:
    scale_factor = 1.8 / max_dim  # Smaller ship to see more background
    ship.scale = (scale_factor, scale_factor, scale_factor)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Slight rotation for dynamic angle
ship.rotation_euler = (math.radians(5), math.radians(-10), math.radians(15))

print(f"Ship dimensions: {ship.dimensions}")

# ============================================
# SPACE BACKGROUND - Your image as environment
# ============================================

print("Setting up space background...")

world = bpy.data.worlds.new(name="Space_HDRI")
bpy.context.scene.world = world
world.use_nodes = True
nodes = world.node_tree.nodes
links = world.node_tree.links
nodes.clear()

tex_coord = nodes.new('ShaderNodeTexCoord')
tex_coord.location = (-800, 0)

mapping = nodes.new('ShaderNodeMapping')
mapping.location = (-600, 0)
mapping.inputs['Rotation'].default_value = (0, 0, 0)

env_tex = nodes.new('ShaderNodeTexEnvironment')
env_tex.location = (-300, 0)
env_tex.image = bpy.data.images.load(r"C:\Users\noahs\Desktop\ai experiments\blender\space background.png")
env_tex.interpolation = 'Smart'

background = nodes.new('ShaderNodeBackground')
background.location = (0, 0)
background.inputs['Strength'].default_value = 1.0

output = nodes.new('ShaderNodeOutputWorld')
output.location = (300, 0)

links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
links.new(mapping.outputs['Vector'], env_tex.inputs['Vector'])
links.new(env_tex.outputs['Color'], background.inputs['Color'])
links.new(background.outputs['Background'], output.inputs['Surface'])

# ============================================
# CYBERPUNK SHIP MATERIAL
# ============================================

print("Creating cyberpunk materials...")

def create_cyberpunk_hull():
    """Dark worn metal with neon accent lighting"""
    mat = bpy.data.materials.new(name="Cyberpunk_Hull")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Texture coordinates
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1200, 0)
    
    # Worn metal noise
    noise1 = nodes.new('ShaderNodeTexNoise')
    noise1.location = (-900, 200)
    noise1.inputs['Scale'].default_value = 30
    noise1.inputs['Detail'].default_value = 10
    noise1.inputs['Roughness'].default_value = 0.7
    
    # Scratches/wear pattern
    noise2 = nodes.new('ShaderNodeTexNoise')
    noise2.location = (-900, -100)
    noise2.inputs['Scale'].default_value = 100
    noise2.inputs['Detail'].default_value = 15
    noise2.inputs['Roughness'].default_value = 0.9
    
    # Edge wear using voronoi
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-900, -400)
    voronoi.inputs['Scale'].default_value = 50
    voronoi.feature = 'DISTANCE_TO_EDGE'
    
    # Color ramp for base - dark gunmetal
    ramp_base = nodes.new('ShaderNodeValToRGB')
    ramp_base.location = (-600, 200)
    ramp_base.color_ramp.elements[0].color = (0.015, 0.018, 0.025, 1)  # Near black
    ramp_base.color_ramp.elements[1].color = (0.04, 0.045, 0.06, 1)    # Dark blue-gray
    
    # Color ramp for scratches - lighter worn areas
    ramp_scratches = nodes.new('ShaderNodeValToRGB')
    ramp_scratches.location = (-600, -100)
    ramp_scratches.color_ramp.elements[0].position = 0.4
    ramp_scratches.color_ramp.elements[0].color = (0.03, 0.035, 0.045, 1)
    ramp_scratches.color_ramp.elements[1].position = 0.6
    ramp_scratches.color_ramp.elements[1].color = (0.08, 0.085, 0.1, 1)  # Worn lighter metal
    
    # Mix base and scratches
    mix_color = nodes.new('ShaderNodeMixRGB')
    mix_color.location = (-300, 100)
    mix_color.blend_type = 'MIX'
    mix_color.inputs['Fac'].default_value = 0.3
    
    # Roughness variation
    ramp_rough = nodes.new('ShaderNodeValToRGB')
    ramp_rough.location = (-600, -400)
    ramp_rough.color_ramp.elements[0].color = (0.5, 0.5, 0.5, 1)
    ramp_rough.color_ramp.elements[1].color = (0.8, 0.8, 0.8, 1)
    
    # Principled BSDF
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (0, 0)
    principled.inputs['Metallic'].default_value = 0.85
    principled.inputs['Specular IOR Level'].default_value = 0.5
    
    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    # Connect
    links.new(tex_coord.outputs['Object'], noise1.inputs['Vector'])
    links.new(tex_coord.outputs['Object'], noise2.inputs['Vector'])
    links.new(tex_coord.outputs['Object'], voronoi.inputs['Vector'])
    links.new(noise1.outputs['Fac'], ramp_base.inputs['Fac'])
    links.new(noise2.outputs['Fac'], ramp_scratches.inputs['Fac'])
    links.new(ramp_base.outputs['Color'], mix_color.inputs['Color1'])
    links.new(ramp_scratches.outputs['Color'], mix_color.inputs['Color2'])
    links.new(mix_color.outputs['Color'], principled.inputs['Base Color'])
    links.new(voronoi.outputs['Distance'], ramp_rough.inputs['Fac'])
    links.new(ramp_rough.outputs['Color'], principled.inputs['Roughness'])
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_neon_accent():
    """Cyberpunk neon glow accents"""
    mat = bpy.data.materials.new(name="Neon_Accent")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (0, 0)
    principled.inputs['Base Color'].default_value = (0, 0.8, 0.9, 1)  # Cyan
    principled.inputs['Emission Color'].default_value = (0, 1, 1, 1)
    principled.inputs['Emission Strength'].default_value = 5
    principled.inputs['Roughness'].default_value = 0.3
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

# Clear existing materials and apply cyberpunk hull
ship.data.materials.clear()
hull_mat = create_cyberpunk_hull()
ship.data.materials.append(hull_mat)

# ============================================
# LIGHTING - Dramatic cyberpunk style
# ============================================

print("Setting up cyberpunk lighting...")

# Key light - cool white from planet direction (top right)
bpy.ops.object.light_add(type='SUN', location=(5, 5, 8))
key_light = bpy.context.active_object
key_light.name = "Key_Light"
key_light.data.energy = 1.5
key_light.data.color = (0.9, 0.95, 1.0)  # Cool white
key_light.data.angle = math.radians(1)
key_light.rotation_euler = (math.radians(55), math.radians(10), math.radians(40))

# Cyan rim light - cyberpunk signature
bpy.ops.object.light_add(type='AREA', location=(-4, 3, 1))
cyan_rim = bpy.context.active_object
cyan_rim.name = "Cyan_Rim"
cyan_rim.data.energy = 150
cyan_rim.data.color = (0, 0.9, 1)  # Cyan
cyan_rim.data.size = 2
cyan_rim.rotation_euler = (math.radians(80), 0, math.radians(-150))

# Magenta/pink accent - cyberpunk contrast
bpy.ops.object.light_add(type='AREA', location=(3, -4, -1))
pink_accent = bpy.context.active_object
pink_accent.name = "Pink_Accent"
pink_accent.data.energy = 80
pink_accent.data.color = (1, 0.2, 0.6)  # Hot pink/magenta
pink_accent.data.size = 3
pink_accent.rotation_euler = (math.radians(100), 0, math.radians(30))

# Very subtle blue fill
bpy.ops.object.light_add(type='AREA', location=(0, -6, 0))
fill = bpy.context.active_object
fill.name = "Fill"
fill.data.energy = 20
fill.data.color = (0.3, 0.4, 0.8)
fill.data.size = 8
fill.rotation_euler = (math.radians(90), 0, 0)

# ============================================
# CAMERA - Wide shot to see full background
# ============================================

print("Setting up camera...")

bpy.ops.object.camera_add(location=(-5, -6, 1.5))
camera = bpy.context.active_object
camera.name = "Main_Camera"

# Look at ship
direction = ship.location - camera.location
rot_quat = direction.to_track_quat('-Z', 'Y')
camera.rotation_euler = rot_quat.to_euler()

bpy.context.scene.camera = camera
camera.data.lens = 35  # Wider lens to see more background
camera.data.clip_end = 1000

# Subtle DOF
camera.data.dof.use_dof = True
camera.data.dof.focus_object = ship
camera.data.dof.aperture_fstop = 11  # Deeper focus

# ============================================
# RENDER SETTINGS
# ============================================

print("Configuring render...")

scene = bpy.context.scene
scene.render.engine = 'CYCLES'

try:
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
    bpy.context.scene.cycles.device = 'GPU'
    bpy.context.preferences.addons['cycles'].preferences.get_devices()
    for device in bpy.context.preferences.addons['cycles'].preferences.devices:
        device.use = True
except:
    scene.cycles.device = 'CPU'

scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100

scene.cycles.samples = 512
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPENIMAGEDENOISE'

# Cyberpunk color grading - high contrast, slight teal push
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Very High Contrast'
scene.view_settings.exposure = 0.0
scene.view_settings.gamma = 1.0

# Bloom/glare handled via Cycles settings instead
scene.cycles.film_exposure = 1.0

# Output
scene.render.filepath = r"C:\Users\noahs\Desktop\ai experiments\blender\cyberpunk_ship_render.png"
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.image_settings.color_depth = '16'

# ============================================
# RENDER
# ============================================

print("Rendering cyberpunk scene...")
bpy.ops.render.render(write_still=True)

print(f"\nDone! Render saved to: {scene.render.filepath}")
