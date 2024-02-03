import java.util.HashMap;
import java.util.Map;

public class Node {
	private String name;
	private boolean isVisited = false;
	private boolean isVisitedBFS = false;
	private Map<Node, Integer> adjacencyMap = new HashMap<>();

	public Node(String name) {
		this.name = name;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public Map<Node, Integer> getAdjacencyMap() {
		return adjacencyMap;
	}

	public void setAdjacencyMap(Map<Node, Integer> adjacencyMap) {
		this.adjacencyMap = adjacencyMap;
	}

	public boolean isVisited() {
		return isVisited;
	}

	public void setVisited(boolean isVisited) {
		this.isVisited = isVisited;
	}

	public boolean isVisitedBFS() {
		return isVisitedBFS;
	}

	public void setVisitedBFS(boolean isVisitedBFS) {
		this.isVisitedBFS = isVisitedBFS;
	}
	
}
