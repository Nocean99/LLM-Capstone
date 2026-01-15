import bpy
import math
import random

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# ============================================
# STAR DESTROYER MODEL (Stylized Imperial-class)
# ============================================

def create_star_destroyer():
    """Create a stylized Star Destroyer using geometric shapes"""
    
    # Main hull - wedge shape using a cone with 4 vertices
    bpy.ops.mesh.primitive_cone_add(
        vertices=4,
        radius1=0,
        radius2=3,
        depth=12,
        location=(0, 0, 0),
        rotation=(math.radians(90), 0, math.radians(45))
    )
    hull = bpy.context.active_object
    hull.name = "SD_Hull"
    
    # Scale to create the wedge shape
    hull.scale = (1, 0.15, 1)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    
    # Bridge tower base
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(3.5, 0, 0.4)
    )
    bridge_base = bpy.context.active_object
    bridge_base.name = "SD_BridgeBase"
    bridge_base.scale = (0.8, 0.6, 0.3)
    
    # Bridge tower
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(3.5, 0, 0.8)
    )
    bridge = bpy.context.active_object
    bridge.name = "SD_Bridge"
    bridge.scale = (0.4, 0.4, 0.35)
    
    # Shield generator domes (left and right)
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.15,
            location=(3.5, side * 0.35, 1.1)
        )
        dome = bpy.context.active_object
        dome.name = f"SD_Dome_{side}"
        dome.scale = (1, 1, 0.7)
    
    # Engine block
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(5.5, 0, 0)
    )
    engines = bpy.context.active_object
    engines.name = "SD_Engines"
    engines.scale = (0.5, 1.2, 0.3)
    
    # Engine glow spheres
    for i in range(3):
        for j in range(2):
            bpy.ops.mesh.primitive_uv_sphere_add(
                radius=0.12,
                location=(5.8, -0.4 + j * 0.8, -0.1 + i * 0.15)
            )
            engine_glow = bpy.context.active_object
            engine_glow.name = f"SD_EngineGlow_{i}_{j}"
    
    # Surface detail - trenches (using cubes with dark material)
    for i in range(5):
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(i * 1.5 - 2, 0, 0.18)
        )
        trench = bpy.context.active_object
        trench.name = f"SD_Trench_{i}"
        trench.scale = (0.05, 2 - i * 0.3, 0.02)
    
    # Select all Star Destroyer parts
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.data.objects:
        if obj.name.startswith("SD_"):
            obj.select_set(True)
    
    # Set hull as active and join
    bpy.context.view_layer.objects.active = hull
    bpy.ops.object.join()
    
    star_destroyer = bpy.context.active_object
    star_destroyer.name = "StarDestroyer"
    
    return star_destroyer

# ============================================
# MATERIALS
# ============================================

def create_hull_material():
    """Sleek metallic hull material"""
    mat = bpy.data.materials.new(name="Hull_Material")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    nodes.clear()
    
    # Principled BSDF for PBR material
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (0, 0)
    principled.inputs['Base Color'].default_value = (0.35, 0.37, 0.4, 1)  # Blue-gray
    principled.inputs['Metallic'].default_value = 0.7
    principled.inputs['Roughness'].default_value = 0.3
    principled.inputs['Specular IOR Level'].default_value = 0.5
    
    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_engine_glow_material():
    """Blue engine glow emission material"""
    mat = bpy.data.materials.new(name="Engine_Glow")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    nodes.clear()
    
    emission = nodes.new('ShaderNodeEmission')
    emission.location = (0, 0)
    emission.inputs['Color'].default_value = (0.3, 0.6, 1, 1)  # Blue
    emission.inputs['Strength'].default_value = 50
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    
    return mat

# ============================================
# SPACE ENVIRONMENT
# ============================================

def create_starfield():
    """Create a starfield background using world shader"""
    world = bpy.data.worlds.new(name="Space")
    bpy.context.scene.world = world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links
    
    nodes.clear()
    
    # Background
    background = nodes.new('ShaderNodeBackground')
    background.location = (0, 0)
    background.inputs['Color'].default_value = (0.001, 0.001, 0.005, 1)  # Deep space blue-black
    background.inputs['Strength'].default_value = 1
    
    # Output
    output = nodes.new('ShaderNodeOutputWorld')
    output.location = (300, 0)
    
    links.new(background.outputs['Background'], output.inputs['Surface'])
    
    # Add star particles
    for i in range(200):
        x = random.uniform(-50, 50)
        y = random.uniform(-50, 50)
        z = random.uniform(-50, 50)
        
        # Keep stars away from the ship area
        if abs(x) < 15 and abs(y) < 15 and abs(z) < 5:
            continue
            
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=random.uniform(0.02, 0.08),
            location=(x, y, z)
        )
        star = bpy.context.active_object
        star.name = f"Star_{i}"
        
        # Star emission material
        star_mat = bpy.data.materials.new(name=f"Star_Mat_{i}")
        star_mat.use_nodes = True
        star_nodes = star_mat.node_tree.nodes
        star_links = star_mat.node_tree.links
        star_nodes.clear()
        
        emission = star_nodes.new('ShaderNodeEmission')
        # Random star colors (white, blue-white, yellow)
        color_choice = random.choice([
            (1, 1, 1, 1),
            (0.8, 0.9, 1, 1),
            (1, 0.95, 0.8, 1)
        ])
        emission.inputs['Color'].default_value = color_choice
        emission.inputs['Strength'].default_value = random.uniform(5, 20)
        
        output = star_nodes.new('ShaderNodeOutputMaterial')
        star_links.new(emission.outputs['Emission'], output.inputs['Surface'])
        
        star.data.materials.append(star_mat)

# ============================================
# LIGHTING
# ============================================

def setup_lighting():
    """Create dramatic space lighting"""
    
    # Key light (sun) - represents distant star
    bpy.ops.object.light_add(
        type='SUN',
        location=(10, -10, 10)
    )
    sun = bpy.context.active_object
    sun.name = "KeyLight_Sun"
    sun.data.energy = 3
    sun.data.color = (1, 0.95, 0.9)
    sun.rotation_euler = (math.radians(45), math.radians(30), math.radians(45))
    
    # Rim light - blue fill from behind
    bpy.ops.object.light_add(
        type='AREA',
        location=(-8, 5, 2)
    )
    rim = bpy.context.active_object
    rim.name = "RimLight"
    rim.data.energy = 500
    rim.data.color = (0.6, 0.8, 1)
    rim.data.size = 5
    rim.rotation_euler = (math.radians(90), 0, math.radians(-120))
    
    # Fill light - subtle ambient
    bpy.ops.object.light_add(
        type='AREA',
        location=(0, -8, -2)
    )
    fill = bpy.context.active_object
    fill.name = "FillLight"
    fill.data.energy = 100
    fill.data.color = (0.4, 0.4, 0.5)
    fill.data.size = 8

# ============================================
# CAMERA
# ============================================

def setup_camera():
    """Position camera for dramatic angle"""
    bpy.ops.object.camera_add(
        location=(-8, -12, 4)
    )
    camera = bpy.context.active_object
    camera.name = "RenderCamera"
    
    # Point at the Star Destroyer
    camera.rotation_euler = (math.radians(70), 0, math.radians(-30))
    
    # Set as active camera
    bpy.context.scene.camera = camera
    
    # Camera settings
    camera.data.lens = 35
    camera.data.clip_end = 1000

# ============================================
# RENDER SETTINGS
# ============================================

def setup_render():
    """Configure render settings for quality output"""
    scene = bpy.context.scene
    
    # Use Cycles for realistic rendering
    scene.render.engine = 'CYCLES'
    
    # GPU if available, otherwise CPU
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
    bpy.context.scene.cycles.device = 'GPU'
    
    # Render settings
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    
    # Cycles settings
    scene.cycles.samples = 256
    scene.cycles.use_denoising = True
    
    # Output
    scene.render.filepath = "C:\\Users\\noahs\\Desktop\\ai experiments\\blender\\star_destroyer_render.png"
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'

# ============================================
# MAIN EXECUTION
# ============================================

print("Creating Star Destroyer...")
star_destroyer = create_star_destroyer()

print("Applying materials...")
hull_mat = create_hull_material()
star_destroyer.data.materials.append(hull_mat)

print("Creating space environment...")
create_starfield()

print("Setting up lighting...")
setup_lighting()

print("Configuring camera...")
setup_camera()

print("Setting up render...")
setup_render()

print("Rendering...")
bpy.ops.render.render(write_still=True)

print(f"Done! Render saved to: C:\\Users\\noahs\\star_destroyer_render.png")
