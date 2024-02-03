import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class project4 {
	public static void main(String[] args) {
		try {
			File readObject = new File(args[0]); // args[0] = input dir
		    BufferedReader myReader = new BufferedReader(new FileReader(readObject));
		    FileWriter myWriter = new FileWriter(args[1]);
		    int numOfNodes = Integer.valueOf(myReader.readLine());
		    int numOfFlags = Integer.valueOf(myReader.readLine());
		    
		    String[] temp = myReader.readLine().split(" ");
		    String startPoint = temp[0];
		    String endPoint = temp[1];
		    
		    String[] flags = myReader.readLine().split(" ");
		    
		    HashMap<String, Node> nodeMap = new HashMap<>();
		    List<Node> nodeList = new ArrayList<>();
		    for(int k = 0; k< numOfNodes; k++) {
		    	temp = myReader.readLine().split(" ");
		    	Node n = null;
		    	if(nodeMap.containsKey(temp[0])) {
		    		n = nodeMap.get(temp[0]);
		    	} else {
		    		n = new Node(temp[0], false, new HashMap<>());	
		    	}
		    	for(int i = 1; i<temp.length; i+=2) {
		    		Node adjNode = null;
		    		if(nodeMap.containsKey(temp[i])) {
		    			adjNode = nodeMap.get(temp[i]);
			    	} else {
			    		adjNode = new Node(temp[i], false, new HashMap<>());	
			    	}
		    		n.getAdjacencyMap().put(adjNode, Integer.valueOf(temp[i+1]));
		    		adjNode.getAdjacencyMap().put(n, Integer.valueOf(temp[i+1]));
		    		nodeMap.put(temp[i], adjNode);
		    	}
		    	nodeMap.put(temp[0], n);
		    	nodeList.add(n);
		    }
		    
		    Node flagToStart = null;
		    for(String s : flags) {
		    	if(flagToStart == null)
		    		flagToStart = nodeMap.get(s);
		    	nodeMap.get(s).setHasFlag(true);
		    }
		    
		    Graph graph = new Graph(nodeList, numOfNodes, numOfFlags);
		    int shortestPath = graph.dijkstra(nodeMap.get(startPoint), nodeMap.get(endPoint));
		    nodeMap = null;

		    int shortestForFlags = 0;
		    
		    if(numOfFlags > 1) {
		    	shortestForFlags = graph.flagCollector(flagToStart, numOfFlags);
		    } else if(numOfFlags == 1) {
		    	shortestForFlags = 0;
		    } else {
		    	shortestForFlags = -1;
		    }
		    	
		    myWriter.write(String.valueOf(shortestPath)+"\n");
		    myWriter.write(String.valueOf(shortestForFlags));
		    myReader.close();
		    myWriter.close();
		} catch (IOException e) {
		    e.printStackTrace();
		}
	}
}
