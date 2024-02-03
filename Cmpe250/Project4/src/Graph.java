import java.util.AbstractMap;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;

public class Graph {
	private List<Node> nodes;
	private int numOfNodes;
	private int numOfFlags;
	
	private PriorityQueue<Node> pq = new PriorityQueue<>(new NodeComparator());
	
	public Graph(List<Node> nodes, int numOfNodes, int numOfFlags) {
		this.nodes = nodes;
		this.numOfNodes = numOfNodes;
		this.numOfFlags = numOfFlags;
	}
	public List<Node> getNodes() {
		return nodes;
	}
	public void setNodes(List<Node> nodes) {
		this.nodes = nodes;
	}
	public int getNumOfNodes() {
		return numOfNodes;
	}
	public void setNumOfNodes(int numOfNodes) {
		this.numOfNodes = numOfNodes;
	}
	public int getNumOfFlags() {
		return numOfFlags;
	}
	public void setNumOfFlags(int numOfFlags) {
		this.numOfFlags = numOfFlags;
	}
	
    private void handleAdjacent(Node n) {
        int edgeDistance = -1;
        int newDistance = -1;
 
        for (Node adjNode : n.getAdjacencyMap().keySet()) {
            if (!adjNode.isFound()) {
                edgeDistance = n.getAdjacencyMap().get(adjNode);
                newDistance = n.getDistanceToStart() + edgeDistance;
 
                if (adjNode.getDistanceToStart() == Integer.MAX_VALUE || newDistance < adjNode.getDistanceToStart()) {
                	adjNode.setDistanceToStart(newDistance);
                }
                pq.add(adjNode);
            }
        }
    }  
	
	public int dijkstra(Node from, Node to) {
		pq = new PriorityQueue<>(new NodeComparator());
		pq.add(from);
		from.setDistanceToStart(0);
		int foundNodes = 0;
		
		while (foundNodes != numOfNodes) {
            if (pq.isEmpty())
                return -1;
            Node node = pq.poll();
 
            if (node.isFound())
                continue;
            
            node.setFound(true);
            foundNodes++;
            handleAdjacent(node);
        }
		if(to.getDistanceToStart() == Integer.MAX_VALUE) return -1;  // Sonradan ekledim HATA2
		return to.getDistanceToStart();
	}
	
	public Map.Entry<Node, Integer> dijkstraForFlags(Node from) { 
		pq = new PriorityQueue<>(new NodeComparator());
		pq.add(from);
		
        Node minNode = null;
        int minDist = Integer.MAX_VALUE;
        
        for(Node n : nodes) {
        	n.setDistanceToStart(Integer.MAX_VALUE);
        	n.setFound(false);
        }
        
		from.setDistanceToStart(0);
		int foundNodes = 0;

		while (foundNodes != numOfNodes) {
            if (pq.isEmpty())
                return null;
            Node u = pq.poll();
 
            if (u.isFound())
                continue;
            
            u.setFound(true);
            foundNodes++;
            handleAdjacent(u);
            if(u.getDistanceToStart() < minDist && !u.equals(from) && u.getDistanceToStart() != 0 && !u.isVisitedFlag() && u.getHasFlag()) {
        		minDist = u.getDistanceToStart();
        		minNode = u;
        	}
        }
		
		if(minDist == Integer.MAX_VALUE) {
			return null;
		}
		return new AbstractMap.SimpleEntry<>(minNode,minDist);
	}
	
	public int flagCollector(Node start, int numOfFlag) {
		int shortestFlagPath = 0;
		Node n = start;
		int visitedFlags = 0;
		
		while(visitedFlags < numOfFlag) {
			n.setVisitedFlag(true);
			visitedFlags++;
			Map.Entry<Node, Integer> res = dijkstraForFlags(n);
			if(res == null) break;
			shortestFlagPath += res.getValue();
			start = n;
			n = res.getKey();
			start.getAdjacencyMap().put(n, 0);
			n.getAdjacencyMap().put(start, 0);
		}
		System.out.println(visitedFlags);
		if(shortestFlagPath == 0) return -1;
		if(numOfFlags != visitedFlags) return -1; // Sonradan ekledim HATA1
		return shortestFlagPath;
	}
}
