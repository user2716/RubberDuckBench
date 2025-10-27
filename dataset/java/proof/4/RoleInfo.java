import java.io.Serializable;

public class RoleInfo implements Serializable {
    
    private static final long serialVersionUID = 5946986388047856568L;

    private String role;
    private String username;

    public RoleInfo(String role, String username) {
        this.role = role;
        this.username = username;
    }
    
    public String getRole() {
        return role;
    }
    
    public void setRole(String role) {
        this.role = role;
    }
    
    public String getUsername() {
        return username;
    }
    
    public void setUsername(String username) {
        this.username = username;
    }
    
    @Override
    public String toString() {
        return "RoleInfo{" + "role='" + role + '\'' + ", username='" + username + '\'' + '}';
    }
}
