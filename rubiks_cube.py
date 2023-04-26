from manim import *

class RubiksCube(Scene):
    def construct(self):
        # Create cube and set its orientation
        cube = Cube().scale(2)
        cube.rotate(45 * DEGREES, RIGHT)
        cube.rotate(45 * DEGREES, OUT)
        
        # Define cube colors
        colors = [RED, BLUE, YELLOW, GREEN, ORANGE, WHITE]
        
        # Create color face labels
        labels = []
        for i, color in enumerate(colors):
            label = Text(str(i+1))
            label.set_color(color)
            label.scale(1.5)
            labels.append(label)
        
        # Position face labels
        labels[0].next_to(cube[0], UP, buff=0.1)
        labels[1].next_to(cube[1], LEFT, buff=0.1)
        labels[2].next_to(cube[2], DOWN, buff=0.1)
        labels[3].next_to(cube[3], RIGHT, buff=0.1)
        labels[4].next_to(cube[4], OUT, buff=0.1)
        labels[5].next_to(cube[5], IN, buff=0.1)
        
        # Add cube and labels to scene
        self.add(cube, *labels)
        
        # Animate cube rotation
        self.play(
            cube.animate.rotate(-90 * DEGREES, LEFT),
            cube.animate.rotate(90 * DEGREES, UP),
            cube.animate.rotate(90 * DEGREES, OUT),
            run_time=2
        )
