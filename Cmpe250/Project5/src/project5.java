import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class project5 {
	public static void main(String[] args) {
		try {
			
			File readObject = new File(args[0]);
		    BufferedReader myReader = new BufferedReader(new FileReader(readObject));
		    FileWriter myWriter = new FileWriter(args[1]);
		    
		    int numOfCities = Integer.valueOf(myReader.readLine());
		    String[] numOfTroops = myReader.readLine().split(" ");
		    HashMap<Node, Integer> regions = new HashMap<>();
		    HashMap<String, Node> cities = new HashMap<>();
		    
		    Node source = new Node("source");
		    cities.put("source", source);
		    
		    for(int i=0; i<6; i++) {
		    	String[] data = myReader.readLine().split(" ");
		    	Node r = new Node(data[0]);
		    	for(int j=1; j<data.length; j+=2) {
		    		Node c;
		    		if(!cities.containsKey(data[j])) {
		    			c = new Node(data[j]);
		    			cities.put(data[j], c);
		    		} else {
		    			c = cities.get(data[j]);
		    		}
		    		r.getAdjacencyMap().put(c, Integer.valueOf(data[j+1]));
		    	}
		    	regions.put(r, Integer.valueOf(numOfTroops[i]));
		    	cities.put(data[0], r);
		    	source.getAdjacencyMap().put(r, Integer.valueOf(numOfTroops[i]));
		    }
		    
		    for(int i=0; i<numOfCities; i++) {
		    	String[] data = myReader.readLine().split(" ");
		    	Node c;
	    		if(!cities.containsKey(data[0])) {
	    			c = new Node(data[0]);
	    			cities.put(data[0], c);
	    		} else {
	    			c = cities.get(data[0]);
	    		}
	    		Node city;
	    		for(int j=1; j<data.length; j+=2) {
	    			if(!cities.containsKey(data[j])) {
	    				city = new Node(data[j]);
		    			cities.put(data[j], city);
		    		} else {
		    			city = cities.get(data[j]);
		    		}
	    			c.getAdjacencyMap().put(city, Integer.valueOf(data[j+1]));
	    		}
		    }
		    
		    List<String> result = Graph.fordFulkerson(source, cities.get("KL"), new ArrayList<>(cities.values()));
		    
		    for(int i=0; i<result.size(); i++) {
		    	myWriter.write(result.get(i) + "\n");
		    }
		    
		    myReader.close();
		    myWriter.close();
		} catch (IOException e) {
		    e.printStackTrace();
		}
	}
}
