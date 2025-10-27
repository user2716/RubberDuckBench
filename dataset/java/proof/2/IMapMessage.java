public class IMapMessage extends Message  {
    private String uid;

    public IMapMessage(String uid) { 
       this.uid = uid; 
    }

    public String toString() {
        return uid;
    }

}
