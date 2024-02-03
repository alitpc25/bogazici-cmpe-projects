import java.util.Comparator;
import java.util.Map;

public class Node {
	private String name;
	private boolean hasFlag;
	private Map<Node, Integer> adjacencyMap;
	private int distanceToStart;
	private boolean isFound;
	private boolean isVisitedFlag;
	
	public int getDistanceToStart() {
		return distanceToStart;
	}
	public void setDistanceToStart(int distanceToStart) {
		this.distanceToStart = distanceToStart;
	}
	public Node(String name, boolean hasFlag, Map<Node, Integer> adjacencyMap) {
		this.name = name;
		this.hasFlag = hasFlag;
		this.adjacencyMap = adjacencyMap;
		this.distanceToStart = Integer.MAX_VALUE;
		this.isFound = false;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public boolean getHasFlag() {
		return hasFlag;
	}
	public void setHasFlag(boolean hasFlag) {
		this.hasFlag = hasFlag;
	}
	public Map<Node, Integer> getAdjacencyMap() {
		return adjacencyMap;
	}
	public void setAdjacencyMap(Map<Node, Integer> adjacencyMap) {
		this.adjacencyMap = adjacencyMap;
	}
	public boolean isFound() {
		return isFound;
	}
	public void setFound(boolean isFound) {
		this.isFound = isFound;
	}
	public boolean isVisitedFlag() {
		return isVisitedFlag;
	}
	public void setVisitedFlag(boolean isVisitedFlag) {
		this.isVisitedFlag = isVisitedFlag;
	}
}

class NodeComparator implements Comparator<Node>{
	@Override
	public int compare(Node o1, Node o2) {
        return o1.getDistanceToStart() - o2.getDistanceToStart();
	}
}
