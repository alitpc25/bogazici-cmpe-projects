import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class LinearProbingHashTable {
    private int currentSize;
    private final int maxSize = 1000;
    private String[] keys;
    private ATC[] vals;
    private List<Integer> keySet;
 
    // Constructor of this class
    public LinearProbingHashTable() {
        currentSize = 0;
        keys = new String[maxSize];
        vals = new ATC[maxSize];
        keySet = new ArrayList<>();
    }
    
    public List<Integer> getKeySet() {
    	Collections.sort(keySet);
		return keySet;
	}

	public void makeEmpty() {
        currentSize = 0;
        keys = new String[maxSize];
        vals = new ATC[maxSize];
        keySet = new ArrayList<>();
    }
    
    public int getSize() { return currentSize; }
    
    public boolean contains(String key) {
        return get(key) != null;
    }
    
    public ATC get(String key) {
        int i = hash(key);
        while (keys[i] != null) {
            if (keys[i].equals(key))
                return vals[i];
            i = (i + 1) % maxSize;
        }
        return null;
    }
    
    public ATC getByIndex(int index) {
    	return vals[index];
    }
    
    public int getIndex(String key) {
        int i = hash(key);
        while (keys[i] != null) {
            if (keys[i].equals(key))
                return i;
            i = (i + 1) % maxSize;
        }
        return 0;
    }
    
    private int hash(String key) {
        return stringHashcode(key) % maxSize;
    }
    
    private int stringHashcode(String key) {
    	int result = 0;
		for(int i=0; i<key.length(); i++) {
			result+= key.charAt(i)*Math.pow(31, i); 
		}
		return result;
    }
    
    public int insert(String key, ATC val) {
        int tmp = hash(key);
        int i = tmp;
 
        do {
            if (keys[i] == null) {
                keys[i] = key;
                vals[i] = val;
                keySet.add(i);
                currentSize++;
                return i;
            }
 
            if (keys[i].equals(key)) {
                vals[i] = val;
                return i;
            }
 
            i = (i + 1) % maxSize;
 
        } while (i != tmp);
        return i;
    }

}
