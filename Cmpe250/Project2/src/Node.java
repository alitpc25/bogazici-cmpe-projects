public class Node {
	private String ipAddress;
	private int height;
	private Node left;
	private Node right;
	
	public Node() {}
	
	public Node(String ipAddress) {
		this.ipAddress = ipAddress;
	}
	
	public Node(String ipAddress, int height, Node left, Node right) {
		this.ipAddress = ipAddress;
		this.height = height;
		this.left = left;
		this.right = right;
	}
	public String getIpAddress() {
		return ipAddress;
	}
	public void setIpAddress(String ipAddress) {
		this.ipAddress = ipAddress;
	}
	public int getHeight() {
		return height;
	}
	public void setHeight(int height) {
		this.height = height;
	}
	public Node getLeft() {
		return left;
	}
	public void setLeft(Node left) {
		this.left = left;
	}
	public Node getRight() {
		return right;
	}
	public void setRight(Node right) {
		this.right = right;
	}
}
