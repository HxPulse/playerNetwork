(function () {
    // ---------------- CONFIG ----------------
    const NODE_COLOR = "#60A5FA";
    const EDGE_COLOR = "#64748b";
    const HIGHLIGHT_COLOR = "#EF4444";
    const MIN_MATCHES_FLOOR = 2;      // graph_data.js only contains edges with >= 2 matches
    const STABILIZE_ITERATIONS = 300;

    // ---------------- DOM ----------------
    const $ = id => document.getElementById(id);
    const loadingEl = $("loading");
    const loadingFill = $("loadingFill");
    const loadingText = $("loadingText");
    const manuallyPositionedNodes = new Map();

    const controls = document.getElementById("controls");
    const toggleButton = document.getElementById("toggleControls");

    toggleButton.addEventListener("click", () => {
        const isHidden = controls.style.display === "none";

        controls.style.display = isHidden ? "block" : "none";
        toggleButton.textContent = isHidden ? "Hide controls" : "Show controls";
    });
    // ---------------- LOADING BAR ----------------
    function setProgress(fraction) {
        const pct = Math.round(Math.min(1, Math.max(0, fraction)) * 100);
        loadingFill.style.width = pct + "%";
        loadingText.textContent = pct + "%";
    }

    function showLoading() {
        setProgress(0);
        loadingEl.classList.remove("hidden");
    }

    function hideLoading() {
        setProgress(1);
        loadingEl.classList.add("hidden");
    }

    // ---------------- NETWORK ----------------
    const allNodeData = GRAPH_DATA.nodes;
    const allEdgeData = GRAPH_DATA.edges;

    const nodes = new vis.DataSet();
    const edges = new vis.DataSet();

    const network = new vis.Network($("mynetwork"), { nodes, edges }, {
        nodes: { shape: "dot", color: NODE_COLOR, font: { color: "white" }},
        edges: {
            color: { color: EDGE_COLOR, highlight: EDGE_COLOR, hover: EDGE_COLOR, inherit: false },
            smooth: { enabled: true, type: "dynamic" }
        },
        interaction: { dragNodes: true, hideEdgesOnDrag: false, hideNodesOnDrag: false, selectConnectedEdges: false },
        physics: {
            enabled: true,
            solver: "repulsion",
            repulsion: {
                centralGravity: 0.05,
                damping: 0.10,
                nodeDistance: 750,
                springConstant: 0.015,
                springLength: 220
            },
            // We trigger stabilization ourselves in rebuildGraph()
            stabilization: { enabled: false, fit: true, updateInterval: 25 }
        }
    });

    // These are persistent (on, not once), so the bar works on every regenerate.
    network.on("stabilizationProgress", params => setProgress(params.iterations / params.total));
    network.on("stabilizationIterationsDone", hideLoading);
    // Remember where the user drops a node.
    network.on("dragEnd", params => {
        params.nodes.forEach(nodeId => {
            const position = network.getPositions([nodeId])[nodeId];
            manuallyPositionedNodes.set(nodeId, { x: position.x, y: position.y });
        });
    });

    // Gently pull manually positioned nodes towards their chosen position.
    network.on("afterDrawing", () => {
        manuallyPositionedNodes.forEach((target, nodeId) => {
            const current = network.getPositions([nodeId])[nodeId];
            if (!current) return;

            const dx = target.x - current.x;
            const dy = target.y - current.y;

            if (Math.abs(dx) > 5 || Math.abs(dy) > 5) {
                network.moveNode( nodeId,
                    current.x + dx * 0.08,
                    current.y + dy * 0.08
                );
            }
        });
    });

    // ---------------- GRAPH FILTERING ----------------
    function generateGraph() {
        const minWeight = Number($("minWeight").value);
        const minMatches = Math.max(MIN_MATCHES_FLOOR, Number($("minMatches").value));

        if (!Number.isInteger(minWeight) || minWeight < 0 || !Number.isInteger(minMatches)) {
            alert("Please enter valid non-negative integers.");
            return;
        }

        showLoading();
        // Give the browser a moment to paint the overlay before the heavy work.
        setTimeout(() => rebuildGraph(minWeight, minMatches), 30);
    }

    function rebuildGraph(minWeight, minMatches) {
        manuallyPositionedNodes.clear();
        // 1. Filter connections by matching count.
        const filteredEdges = allEdgeData.filter(edge => edge.value >= minMatches);

        // 2. Total connection weight per player.
        const playerWeights = {};
        filteredEdges.forEach(edge => {
            playerWeights[edge.from] = (playerWeights[edge.from] || 0) + edge.value;
            playerWeights[edge.to] = (playerWeights[edge.to] || 0) + edge.value;
        });

        // 3. Keep players with enough total weight.
        const filteredNodes = allNodeData
            .filter(node => (playerWeights[node.id] || 0) >= minWeight)
            .map(node => {
                const degree = playerWeights[node.id] || 0;

                // Find the player's 5 strongest connections, requiring > 3 matches.
                const topMatches = allEdgeData
                    .filter(edge => (edge.from === node.id || edge.to === node.id) && edge.value >= 3)
                    .sort((a, b) => b.value - a.value)
                    .slice(0, 5)
                    .map(edge => {
                        const opponentId = edge.from === node.id ? edge.to : edge.from;
                        const opponent = allNodeData.find(n => n.id === opponentId);

                        return `${opponent?.label || opponentId}: ${edge.value} matches`;
                    });

                return {
                    ...node,
                    size: Math.min(56, 22 + degree * 0.58),
                    font: {size: 32, color: "white", strokeWidth: 3, strokeColor: "#1e293b"},
                    title: `${node.label}\n${node.id}\nConnections: ${degree}\n\nTop matches:\n${topMatches.join("\n")}`,
                    color: NODE_COLOR
                };
            });

        // 4. Only keep edges between visible players.
        const visibleIds = new Set(filteredNodes.map(node => node.id));
        const finalEdges = filteredEdges
            .filter(edge => visibleIds.has(edge.from) && visibleIds.has(edge.to))
            .map(edge => ({ ...edge, color: EDGE_COLOR }));

        // 5. Replace the displayed graph.
        network.unselectAll();
        edges.clear();
        nodes.clear();
        nodes.add(filteredNodes);
        edges.add(finalEdges);

        $("graphStats").textContent =
            `${filteredNodes.length} players | ${finalEdges.length} connections`;

        // vis never fires "stabilizationIterationsDone" for an empty graph.
        if (filteredNodes.length === 0) {
            hideLoading();
            return;
        }
        network.setOptions({ physics: { enabled: true } });
        network.stabilize(STABILIZE_ITERATIONS);
    }

    // ---------------- HIGHLIGHTING ----------------
    function resetHighlights() {
        nodes.update(nodes.get().map(node => ({ id: node.id, color: NODE_COLOR })));
        edges.update(edges.get().map(edge => ({ id: edge.id, color: EDGE_COLOR })));
    }

    network.on("selectNode", params => {
        if (!params.nodes.length) return;

        resetHighlights();

        const connectedEdges = network.getConnectedEdges(params.nodes[0]);
        if (!connectedEdges.length) return;

        const strongestEdge = connectedEdges
            .map(id => edges.get(id))
            .sort((a, b) => b.value - a.value)[0];

        edges.update({ id: strongestEdge.id, color: HIGHLIGHT_COLOR });
        nodes.update([
            { id: strongestEdge.from, color: HIGHLIGHT_COLOR },
            { id: strongestEdge.to, color: HIGHLIGHT_COLOR }
        ]);
    });

    network.on("deselectNode", resetHighlights);

    // ---------------- PLAYER SEARCH ----------------
    $("playerSearch").addEventListener("keydown", function (event) {
        if (event.key !== "Enter") return;

        const query = this.value.toLowerCase().trim();
        if (!query) return;

        const match = nodes.get().find(node =>
            node.label.toLowerCase().includes(query) ||
            node.id.toLowerCase().includes(query)
        );

        if (!match) {
            alert("Player not found!");
            return;
        }

        network.unselectAll();
        network.focus(match.id, { scale: 1.5, animation: true });
        network.emit("selectNode", { nodes: [match.id] });
    });

    // ---------------- INIT ----------------
    $("generateButton").addEventListener("click", generateGraph);
    generateGraph();
})();