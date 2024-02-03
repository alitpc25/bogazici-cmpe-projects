import java.io.FileWriter;
import java.io.IOException;

public class AVLTree extends BinarySearchTree {
	private Node root;
	private FileWriter writer;
	
	public AVLTree() {
		super();
	}
    
    public AVLTree(String ipAddress, FileWriter writer) {
    	super(ipAddress, writer);
    	this.root = super.getRoot();
    	this.writer = super.getWriter();
    }
    
    // Calls recursive insert function.
    public void insert(String ipAddress) {
    	root = insert(root, ipAddress);
    }
 
    // Recursive function to add new node to the tree.
    private Node insert(Node node, String ipAddress) {
    	if (node == null) {
    		node = new Node(ipAddress);
            return node;
        }
    	try {
			writer.write(node.getIpAddress()+": New node being added with IP:" + ipAddress + "\n");
		} catch (IOException e) {
			e.printStackTrace();
		}
    	int compareResult = ipAddress.compareTo(node.getIpAddress());
        if (compareResult < 0) {
        	node.setLeft(insert(node.getLeft(), ipAddress));
        } else if (compareResult > 0) {
        	node.setRight(insert(node.getRight(), ipAddress));
        } else {
        	return node;
        }
        
        node.setHeight(1 + Math.max(height(node.getLeft()), height(node.getRight()))); // Update height
        int balance = getBalance(node); // To check whether AVL property is preserved.
        // If this node becomes unbalanced, then there are 4 cases
        // Left Left Case
        if (balance > 1 && ipAddress.compareTo(node.getLeft().getIpAddress()) < 0) {
        	try {
    			writer.write("Rebalancing: right rotation" + "\n");
    		} catch (IOException e) {
    			e.printStackTrace();
    		}
            return rightRotate(node);
        }
 
        // Right Right Case
        if (balance < -1 && ipAddress.compareTo(node.getRight().getIpAddress()) > 0) {
        	try {
    			writer.write("Rebalancing: left rotation" + "\n");
    		} catch (IOException e) {
    			e.printStackTrace();
    		}
            return leftRotate(node);
        }
 
        // Left Right Case
        if (balance > 1 && ipAddress.compareTo(node.getLeft().getIpAddress()) > 0) {
        	try {
    			writer.write("Rebalancing: left-right rotation" + "\n");
    		} catch (IOException e) {
    			e.printStackTrace();
    		}
            node.setLeft(leftRotate(node.getLeft()));
            return rightRotate(node);
        }
 
        // Right Left Case
        if (balance < -1 && ipAddress.compareTo(node.getRight().getIpAddress()) < 0) {
        	try {
    			writer.write("Rebalancing: right-left rotation" + "\n");
    		} catch (IOException e) {
    			e.printStackTrace();
    		}
            node.setRight(rightRotate(node.getRight()));
            return leftRotate(node);
        }

        return node;       
    }
    
    public void remove(String x) {
        root = remove(x, root, root, true);
    }
    
    private Node remove(String x, Node t, Node prevHead, boolean shouldWrite) {
        if( t == null )
            return t;   // Item not found; do nothing
        int compareResult = x.compareTo(t.getIpAddress());
        if( compareResult < 0 ) {
        	t.setLeft(remove(x, t.getLeft(),t, shouldWrite));
        } else if( compareResult > 0 ) {
        	t.setRight(remove(x, t.getRight(),t, shouldWrite));
        } else if( t.getLeft() != null && t.getRight() != null ) // Two children
        {
        	String minAddress = findMin(t.getRight()).getIpAddress();
        	if(!x.equals(root.getIpAddress())) {
	        	try {
	    			writer.write(prevHead.getIpAddress() +": Non Leaf Node Deleted; removed: " + x + " replaced: " + minAddress + "\n");
	    		} catch (IOException e) {
	    			e.printStackTrace();
	    		}
        	}
        	t.setIpAddress(minAddress);
            t.setRight(remove(t.getIpAddress(), t.getRight(),t, false));
        } else {
        	t = (t.getLeft() != null) ? t.getLeft() : t.getRight();	
        	if(t != null) { // One child case
        		if(shouldWrite) {
	            	try {
	        			writer.write(prevHead.getIpAddress() + ": Node with single child Deleted: " + x + "\n");
	        		} catch (IOException e) {
	        			e.printStackTrace();
	        		}
        		}
        	} else { // No child case
        		if(shouldWrite) {
	        		try {
	        			writer.write(prevHead.getIpAddress() + ": Leaf Node Deleted: " + x + "\n");
	        		} catch (IOException e) {
	        			e.printStackTrace();
	        		}
        		}
        	}	
        }
        
        if (t == null)
            return t;
        
        t.setHeight(Math.max(height(t.getLeft()), height(t.getRight())) + 1);
        
        int balance = getBalance(t);
        
        // If this node becomes unbalanced, then there are 4 cases
        // Left Left Case
        if (balance > 1 && getBalance(t.getLeft()) >= 0) {
        	try {
    			writer.write("Rebalancing: right rotation" + "\n");
    		} catch (IOException e) {
    			e.printStackTrace();
    		}
            return rightRotate(t);
        }
 
        // Left Right Case
        if (balance > 1 && getBalance(t.getLeft()) < 0) {
        	try {
    			writer.write("Rebalancing: left-right rotation" + "\n");
    		} catch (IOException e) {
    			e.printStackTrace();
    		}
            t.setLeft(leftRotate(t.getLeft()));
            return rightRotate(t);
        }
 
        // Right Right Case
        if (balance < -1 && getBalance(t.getRight()) <= 0) {
        	try {
    			writer.write("Rebalancing: left rotation" + "\n");
    		} catch (IOException e) {
    			e.printStackTrace();
    		}
            return leftRotate(t);
        }
 
        // Right Left Case
        if (balance < -1 && getBalance(t.getRight()) > 0) {
        	try {
    			writer.write("Rebalancing: right-left rotation" + "\n");
    		} catch (IOException e) {
    			e.printStackTrace();
    		}
            t.setRight(rightRotate(t.getRight()));
            return leftRotate(t);
        }
        
        return t;
   
    }
    
    public void sendMessage(String senderIpAddress, String receiverIpAddress) {
    	sendMessage(senderIpAddress, receiverIpAddress, root);
    }
    
    private int height(Node t) {
        if(t == null)
            return -1;
        return t.getHeight();
    }
    
    // Right rotate subtree rooted with y
    private Node rightRotate(Node y) {
        Node x = y.getLeft();
        Node T2 = x.getRight();
 
        // Perform rotation
        x.setRight(y);
        y.setLeft(T2);
 
        // Update heights
        y.setHeight(Math.max(height(y.getLeft()), height(y.getRight())) + 1);
        x.setHeight(Math.max(height(x.getLeft()), height(x.getRight())) + 1);
 
        // Return new root
        return x;
    }
    
    // Left rotate subtree rooted with y
    private Node leftRotate(Node y) {
        Node x = y.getRight();
        Node T2 = x.getLeft();
 
        // Perform rotation
        x.setLeft(y);
        y.setRight(T2);
 
        // Update heights
        y.setHeight(Math.max(height(y.getLeft()), height(y.getRight())) + 1);
        x.setHeight(Math.max(height(x.getLeft()), height(x.getRight())) + 1);
 
        // Return new root
        return x;
    }
    
    // Get Balance factor of node n
    int getBalance(Node n) {
        if (n == null)
            return 0;
        return height(n.getLeft()) - height(n.getRight());
    }
}
