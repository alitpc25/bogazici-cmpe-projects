import java.io.FileWriter;
import java.io.IOException;
import java.util.NoSuchElementException;

public class BinarySearchTree {
	private Node root;
	private FileWriter writer;
    public BinarySearchTree() {
    	root = null; 
    }
    
    public Node getRoot() {
		return root;
	}

	public FileWriter getWriter() {
		return writer;
	}

	public void setRoot(Node root) {
		this.root = root;
	}

	public void setWriter(FileWriter writer) {
		this.writer = writer;
	}

	public BinarySearchTree(String ipAddress, FileWriter writer) {
    	this.root = new Node(ipAddress);
    	this.writer = writer;
    }
    
    // Calls recursive insert function.
    public void insert(String ipAddress) {
    	root = insert(root, ipAddress);
    }
 
    // Recursive function to add new node to the tree.
    private Node insert(Node root, String ipAddress) {
    	if (root == null) {
            return new Node(ipAddress);
        }
    	try {
			writer.write(root.getIpAddress()+": New node being added with IP:" + ipAddress + "\n");
		} catch (IOException e) {
			e.printStackTrace();
		}
    	int compareResult = ipAddress.compareTo(root.getIpAddress());
        if (compareResult < 0) {
            root.setLeft(insert(root.getLeft(), ipAddress));
        } else if (compareResult > 0) {
        	root.setRight(insert(root.getRight(), ipAddress));
        }
        return root;
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
        	if(!x.equals(root.getIpAddress()) || !prevHead.equals(root)) {
	        	try {
	    			writer.write(prevHead.getIpAddress() + ": Non Leaf Node Deleted; removed: " + x + " replaced: " + minAddress + "\n");
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
        return t;
    }

    protected Node findMin(Node t) {
    	if(isEmpty())
            throw new NoSuchElementException();
        if( t == null )
            return null;
        else if(t.getLeft() == null)
            return t;
        return findMin(t.getLeft());
    }
    
    public void sendMessage(String senderIpAddress, String receiverIpAddress) {
    	sendMessage(senderIpAddress, receiverIpAddress, root);
    }
    
    protected void sendMessage(String senderIpAddress, String receiverIpAddress, Node t) {
    	if(t == null)
            return;
    	int compareResultSender = senderIpAddress.compareTo(t.getIpAddress());
    	int compareResultReceiver = receiverIpAddress.compareTo(t.getIpAddress());
    	if(compareResultSender < 0 && compareResultReceiver < 0) { 
    		// Both are at the left subtree.
    		sendMessage(senderIpAddress, receiverIpAddress, t.getLeft());
    	} else if(compareResultSender > 0 && compareResultReceiver > 0) {
    		// Both are at the right subtree.
    		sendMessage(senderIpAddress, receiverIpAddress, t.getRight());
    	} else {
    		// The least common ancestor found.
    		messageSenderPath(senderIpAddress, t, receiverIpAddress);
    		messageReceiverPath(senderIpAddress, t, receiverIpAddress);
    	}
    	
    }
    
    protected Node messageSenderPath(String senderIpAddress, Node t, String receiverIpAddress) {
        if( t == null )
            return null;
        Node prevNode;
        int compareResult = senderIpAddress.compareTo(t.getIpAddress());
        if( compareResult < 0 ) {
        	prevNode = messageSenderPath(senderIpAddress, t.getLeft(), receiverIpAddress);
        } else if(compareResult > 0) {
        	prevNode = messageSenderPath(senderIpAddress, t.getRight(), receiverIpAddress);
        } else {
        	try {
				writer.write(senderIpAddress + ": Sending message to: " + receiverIpAddress + "\n");
			} catch (IOException e) {
				e.printStackTrace();
			}
        	return t;
        }
        if(prevNode != null && !t.getIpAddress().equals(receiverIpAddress)) {
	        try {
	        	writer.write(t.getIpAddress() + ": Transmission from: " + prevNode.getIpAddress() + " receiver: " + receiverIpAddress + " sender:" + senderIpAddress + "\n");
			} catch (IOException e) {
				e.printStackTrace();
			}
        }
        return t;
    }
    
    protected void messageReceiverPath(String senderIpAddress, Node t, String receiverIpAddress) {
    	if( t == null )
            return;
        int compareResult = receiverIpAddress.compareTo(t.getIpAddress());
        if(compareResult == 0) {
        	try {
				writer.write(receiverIpAddress + ": Received message from: " + senderIpAddress + "\n");
			} catch (IOException e) {
				e.printStackTrace();
			}
        	return;
        }
        Node prevNode;
        while(t != null && !t.getIpAddress().equals(receiverIpAddress)) {
        	compareResult = receiverIpAddress.compareTo(t.getIpAddress());
        	prevNode = t;
        	if( compareResult < 0 ) {
        		t = t.getLeft();
        	} else if(compareResult > 0) {
        		t = t.getRight();
        	}
        	if(t != null) {
        		if(t.getIpAddress().equals(receiverIpAddress)) {
	        		try {
						writer.write(receiverIpAddress + ": Received message from: " + senderIpAddress + "\n");
					} catch (IOException e) {
						e.printStackTrace();
					}
	            	break;
        		} else {
		            try {
		            	writer.write(t.getIpAddress() + ": Transmission from: " + prevNode.getIpAddress() + " receiver: " + receiverIpAddress + " sender:" + senderIpAddress + "\n");
					} catch (IOException e) {
						e.printStackTrace();
					}
        		}
        	}
        }
    }
    
    public void makeEmpty() {
        root = null;
    }
    
    public boolean isEmpty() {
        return root == null;
    }
        
}
