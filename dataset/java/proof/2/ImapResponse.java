import java.util.ArrayList;

public class ImapResponse extends ArrayList<Object> {

    private final String tag;

     private ImapResponse(String tag) {
        this.tag = tag;
    }

    public String getTag() {
        return tag;
    }

    public String getKeyedString(String key) {
        return (String)getKeyedValue(key);
    }

    public Object getKeyedValue(String key) {
        for (int i = 0, count = size() - 1; i < count; i++) {
            if (get(i).equals(key)) {
                return get(i + 1);
            }
        }
        return null;
    }

}
