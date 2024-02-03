import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;

public class Graph {
	
	static HashMap<String, String> path = new HashMap<>();
	
    static boolean bfs(Node s, Node t, HashMap<Node, Node> parent, List<Node> cities) {
        
    	for(Node c : cities)
    		c.setVisited(false);
 
        LinkedList<Node> queue = new LinkedList<Node>();
        queue.add(s);
        s.setVisited(true);
        parent.put(s, null);
 
        while (queue.size() != 0) {
            Node u = queue.poll();
            for (Node v : u.getAdjacencyMap().keySet()) {
                if (v.isVisited() == false && u.getAdjacencyMap().get(v) > 0) {
                    if (v.equals(t)) {
                        parent.put(v, u);
                        return true;
                    }
                    queue.add(v);
                    parent.put(v, u);
                    v.setVisited(true);
                }
            }
        }

        return false;
    }
    
    static List<String> fordFulkerson(Node s, Node t, List<Node> cities) {
    	
        Node u, v;
 
        HashMap<Node, Node> parent = new HashMap<>();
 
        int max_flow = 0;

        while (bfs(s, t, parent, cities)) {
            int path_flow = Integer.MAX_VALUE;
            for (v = t; !v.equals(s); v = parent.get(v)) {
                u = parent.get(v);
                path_flow = Math.min(path_flow, u.getAdjacencyMap().get(v));
            }
 
            for (v = t; !v.equals(s); v = parent.get(v)) {
            	u = parent.get(v);
            	u.getAdjacencyMap().put(v, u.getAdjacencyMap().get(v)-path_flow);
                v.getAdjacencyMap().put(u, v.getAdjacencyMap().getOrDefault(u,0)+path_flow);
            }
            max_flow += path_flow;
        }

        // BONUS
        
        bfs(s);
        
        List<String> result = new ArrayList<>();
        result.add(String.valueOf(max_flow));
      
        for (Node n : cities) {
            for (Node a : n.getAdjacencyMap().keySet()) {
                if (n.isVisitedBFS() && !a.isVisitedBFS()) {
                	if(n.getName().equals(s.getName())) {
                		result.add(a.getName());
                	} else {
                		result.add(n.getName() + " "+ a.getName());
                	}
                }
            }
        }
        // BONUS
        
        return result;
    }
    
    private static void bfs(Node s) {
 
        LinkedList<Node> queue = new LinkedList<Node>();
 
        s.setVisitedBFS(true);
        queue.add(s);
 
        while (queue.size() != 0) {
            Node n = queue.poll();
            for (Node u : n.getAdjacencyMap().keySet()) {
    			if (n.getAdjacencyMap().get(u) > 0 && !u.isVisitedBFS()) {
    				u.setVisitedBFS(true);
                    queue.add(u);
    			}
    		}
        }
    }
    
}
