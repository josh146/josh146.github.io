Title: Recipe graph.
slug: recipe-graph
save_as: recipe-graph.html

<script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>

<div id="recipe-graph" style="width: 100%; height: 600px; background-color: rgb(46, 46, 46); border: 1px solid #e0e0e0; border-radius: 8px;">

<script>
    document.addEventListener("DOMContentLoaded", async function() {
        // 1. Fetch the data we generated in Python
        const response = await fetch('/graph.json');
        const graphData = await response.json();

        const nodesDataSet = new vis.DataSet(graphData.nodes);
        const edgesDataSet = new vis.DataSet(graphData.edges);

        const data = {
            nodes: nodesDataSet,
            edges: edgesDataSet
        };
        // 2. Target the container
        const container = document.getElementById('recipe-graph');

        // 3. Configure the Network (Monokai styled!)
        const options = {
            nodes: {
                shape: 'dot',
                size: 16,
                font: {
                    color: '#ddd', // Changed from white to dark charcoal
                    size: 14,
                    face: 'monospace'
                },
                borderWidth: 2,
                color: {
                    border: '#ddd',
                    background: '#97c2fc' // A nice clean blue for the dots
                },
                shadow: false // Shadows sometimes look muddy on pure white
            },
            edges: {
                smooth: {
                    type: 'continuous'
                },
                color: {
                    color: '#999999',     // Default edge color (light grey)
                    highlight: '#333333', // Turns dark when clicked
                    hover: '#333333'
                }
            },
            physics: {
                barnesHut: {
                    gravitationalConstant: -4000, // Make nodes repel each other more strongly
                    centralGravity: 0.1,          // Reduce the pull to the center of the screen
                    springLength: 250,            // Make the lines longer
                    springConstant: 0.04,
                    avoidOverlap: 0.5             // Force nodes to respect each other's personal space
                },
                stabilization: { iterations: 200 }
            },
            interaction: {
                hover: true,
                zoomView: true,
                dragView: true,
            },
            // layout: { hierarchical: { direction: 'UD' } }
        };

        // 4. Initialize the graph
        const network = new vis.Network(container, data, options);

        // 2. THE CLICK ROUTER
        network.on("click", function (params) {
            if (params.nodes.length > 0) {
                const nodeId = params.nodes[0];
                // Because we use a DataSet, we use .get() instead of an array .find()
                const clickedNode = nodesDataSet.get(nodeId); 
                
                if (clickedNode && clickedNode.url) {
                    window.location.href = clickedNode.url;
                }
            }
        });

        // --- THE FADE EFFECT ---
        network.on("hoverNode", function (params) {
            // Force the cursor to a pointer so it feels like a clickable link
            container.style.cursor = 'pointer'; 
            
            const hoveredNodeId = params.node;
            const connectedNodeIds = network.getConnectedNodes(hoveredNodeId);
            const connectedEdgeIds = network.getConnectedEdges(hoveredNodeId);
            const nodesToHighlight = [hoveredNodeId, ...connectedNodeIds];

            // Update Nodes (Fading both shape AND text)
            const nodesUpdate = nodesDataSet.get().map(node => {
                if (nodesToHighlight.includes(node.id)) {
                    return { 
                        id: node.id, 
                        opacity: 1, 
                        font: { color: '#ddd' } // Solid text
                    };
                } else {
                    return { 
                        id: node.id, 
                        opacity: 0.15, 
                        font: { color: 'rgba(51, 51, 51, 0.15)' } // Faded text!
                    }; 
                }
            });
            nodesDataSet.update(nodesUpdate);

            // Update Edges (Hide unconnected lines)
            const edgesUpdate = edgesDataSet.get().map(edge => {
                return { id: edge.id, hidden: !connectedEdgeIds.includes(edge.id) };
            });
            edgesDataSet.update(edgesUpdate);
        });

        // 4. RESTORE THE GRAPH ON MOUSE LEAVE
        network.on("blurNode", function () {
            // Reset the cursor
            container.style.cursor = 'default';
            
            // Restore all nodes and text to full opacity
            const nodesUpdate = nodesDataSet.get().map(node => ({ 
                id: node.id, 
                opacity: 1, 
                font: { color: '#ddd' } 
            }));
            nodesDataSet.update(nodesUpdate);
            
            // Restore all edges
            const edgesUpdate = edgesDataSet.get().map(edge => ({ 
                id: edge.id, 
                hidden: false 
            }));
            edgesDataSet.update(edgesUpdate);
        });
    });
</script>