network.on("selectNode", function(params) {
    const selectedNode = params.nodes[0];

    // Reset all nodes
    nodes.update(
        nodes.get().map(node => ({
            id: node.id,
            color: "#60A5FA"
        }))
    );

    // Reset all edges
    edges.update(
        edges.get().map(edge => ({
            id: edge.id,
            color: edge.originalColor || "#64748b"
        }))
    );

    // Find connected edges
    const connectedEdges = network.getConnectedEdges(selectedNode);

    if (connectedEdges.length === 0) return;

    // Find edge with highest matching count
    const strongestEdge = connectedEdges
        .map(id => edges.get(id))
        .sort((a, b) => b.value - a.value)[0];

    // Highlight the edge
    edges.update({
        id: strongestEdge.id,
        color: "#EF4444"
    });

    // Highlight both players
    nodes.update([
        { id: strongestEdge.from, color: "#EF4444" },
        { id: strongestEdge.to, color: "#EF4444" }
    ]);
});

// Create search bar
const searchContainer = document.createElement("div");

searchContainer.style = `
    position: fixed;
    top: 20px;
    left: 20px;
    z-index: 1000;
`;

searchContainer.innerHTML = `
    <input
        id="playerSearch"
        type="text"
        placeholder="Search player name or tag..."
        style="
            padding: 12px;
            width: 280px;
            background: #1f2937;
            color: white;
            border: 1px solid #475569;
            border-radius: 8px;
            font-size: 15px;
            outline: none;
        "
    />
`;

document.body.appendChild(searchContainer);

const searchInput = document.getElementById("playerSearch");

searchInput.addEventListener("keydown", function(event) {
    if (event.key !== "Enter") return;

    const query = searchInput.value.toLowerCase().trim();

    if (!query) return;

    const match = nodes.get().find(node =>
        node.label.toLowerCase().includes(query) ||
        node.id.toLowerCase().includes(query)
    );

    if (!match) {
        alert("Player not found!");
        return;
    }

    // Reset colors
    nodes.update(nodes.get().map(node => ({
        id: node.id,
        color: "#60A5FA"
    })));

    edges.update(edges.get().map(edge => ({
        id: edge.id,
        color: edge.originalColor || "#64748b"
    })));

    // Highlight player
    nodes.update({
        id: match.id,
        color: "#EF4444"
    });

    // Center graph on player
    network.focus(match.id, {
        scale: 1.5,
        animation: true
    });
});