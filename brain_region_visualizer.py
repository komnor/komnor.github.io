import numpy as np
import plotly.graph_objects as go

class BrainRegionVisualizer:
    """
    Class for visualizing brain regions related to cross-modal plasticity
    """
    
    def __init__(self):
        # Define brain region coordinates
        self.regions = {
            'v1': {  # Primary Visual Cortex
                'center': [-40, -30, -20],
                'size': [30, 25, 15],
                'color': 'rgba(255, 0, 0, 0.7)',
                'name': 'Primary Visual Cortex (V1)'
            },
            'v2-v5': {  # Secondary Visual Areas
                'center': [-35, -25, -5],
                'size': [25, 20, 15],
                'color': 'rgba(255, 100, 100, 0.7)',
                'name': 'Secondary Visual Areas (V2-V5)'
            },
            'a1': {  # Primary Auditory Cortex
                'center': [10, 50, -10],
                'size': [20, 15, 15],
                'color': 'rgba(0, 0, 255, 0.7)',
                'name': 'Primary Auditory Cortex (A1)'
            },
            'a2': {  # Secondary Auditory Areas
                'center': [15, 40, 0],
                'size': [15, 15, 15],
                'color': 'rgba(100, 100, 255, 0.7)',
                'name': 'Secondary Auditory Areas'
            },
            'association': {  # Association Areas
                'center': [-10, 10, 0],
                'size': [20, 20, 15],
                'color': 'rgba(100, 255, 100, 0.7)',
                'name': 'Association Areas'
            },
            'thalamus': {  # Thalamus
                'center': [0, 0, 0],
                'size': [10, 10, 10],
                'color': 'rgba(255, 255, 0, 0.7)',
                'name': 'Thalamus'
            }
        }
        
        # Define activation levels for each region (0-1)
        self.activation = {region: 0.0 for region in self.regions}
    
    def generate_brain_surface(self):
        """Generate a 3D surface for the brain"""
        # Create a simple ellipsoid for the brain
        u = np.linspace(0, 2*np.pi, 30)
        v = np.linspace(0, np.pi, 30)
        x = 50 * np.outer(np.cos(u), np.sin(v))
        y = 65 * np.outer(np.sin(u), np.sin(v))
        z = 50 * np.outer(np.ones(np.size(u)), np.cos(v))
        
        # Create the brain surface
        brain = go.Surface(
            x=x, y=y, z=z,
            colorscale='Greys',
            opacity=0.4,
            showscale=False,
            hoverinfo='skip',
            name='Brain Surface'
        )
        
        return brain
    
    def generate_region_visualization(self, region_id, activation_level=None):
        """Generate a 3D visualization for a specific brain region"""
        if region_id not in self.regions:
            return None
        
        region = self.regions[region_id]
        
        # Use provided activation level or default to stored value
        if activation_level is not None:
            self.activation[region_id] = activation_level
        
        # Adjust opacity based on activation level
        opacity = 0.3 + 0.7 * self.activation[region_id]
        
        # Create points for the region
        center = region['center']
        size = region['size']
        
        # Create a 3D scatter plot for the region
        x, y, z = [], [], []
        
        # Generate points within an ellipsoid
        for i in range(100):
            # Random points within a unit sphere
            theta = np.random.uniform(0, 2*np.pi)
            phi = np.random.uniform(0, np.pi)
            r = np.random.uniform(0, 1)**(1/3)  # Cube root for uniform distribution in sphere
            
            # Convert to Cartesian coordinates
            px = r * np.sin(phi) * np.cos(theta)
            py = r * np.sin(phi) * np.sin(theta)
            pz = r * np.cos(phi)
            
            # Scale and translate to region position
            x.append(center[0] + px * size[0])
            y.append(center[1] + py * size[1])
            z.append(center[2] + pz * size[2])
        
        # Create the scatter plot
        region_viz = go.Scatter3d(
            x=x, y=y, z=z,
            mode='markers',
            marker=dict(
                size=5,
                color=region['color'],
                opacity=opacity
            ),
            name=region['name'],
            hoverinfo='name'
        )
        
        return region_viz
    
    def set_activation(self, region_id, level):
        """Set activation level for a specific region"""
        if region_id in self.regions and 0 <= level <= 1:
            self.activation[region_id] = level
    
    def reset_activation(self):
        """Reset all activation levels to zero"""
        for region in self.activation:
            self.activation[region] = 0.0
    
    def simulate_auditory_activation(self, intensity=0.8):
        """Simulate activation pattern from auditory stimulus"""
        # Primary auditory cortex activates first
        self.activation['a1'] = intensity
        
        # Secondary auditory areas activate next
        self.activation['a2'] = intensity * 0.9
        
        # Association areas activate as intermediaries
        self.activation['association'] = intensity * 0.7
        
        # Thalamus activates as relay
        self.activation['thalamus'] = intensity * 0.6
        
        # Visual cortex activates through cross-modal connections
        self.activation['v2-v5'] = intensity * 0.5
        self.activation['v1'] = intensity * 0.4
    
    def get_all_regions_visualization(self, selected_regions=None):
        """Get visualization for all selected regions"""
        if selected_regions is None:
            selected_regions = list(self.regions.keys())
        
        # Start with the brain surface
        data = [self.generate_brain_surface()]
        
        # Add each selected region
        for region_id in selected_regions:
            if region_id in self.regions:
                region_viz = self.generate_region_visualization(region_id)
                if region_viz:
                    data.append(region_viz)
        
        return data
    
    def get_brain_layout(self):
        """Get the layout for the brain visualization"""
        layout = go.Layout(
            scene=dict(
                xaxis=dict(title='', showticklabels=False, showgrid=False, zeroline=False),
                yaxis=dict(title='', showticklabels=False, showgrid=False, zeroline=False),
                zaxis=dict(title='', showticklabels=False, showgrid=False, zeroline=False),
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            margin=dict(l=0, r=0, b=0, t=0),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        return layout
    
    def get_complete_figure(self, selected_regions=None):
        """Get complete figure with all visualizations"""
        data = self.get_all_regions_visualization(selected_regions)
        layout = self.get_brain_layout()
        
        return {'data': data, 'layout': layout}
