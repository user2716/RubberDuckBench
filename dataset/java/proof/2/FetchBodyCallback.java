import java.util.Map;

public class FetchBodyCallback {
    private Map<String, Message> mMessageMap;

    public FetchBodyCallback(Map<String, Message> messageMap) {
        mMessageMap = messageMap;
    }

    public Object foundLiteral(ImapResponse response) {

        if (response.getTag() == null && response.get(1).equals("FETCH")) {
            ImapResponse fetchList = (ImapResponse)response.getKeyedValue("FETCH");
            String uid = fetchList.getKeyedString("UID");

            // Only usage of the Hash/Singleton map
            IMapMessage message = (IMapMessage) mMessageMap.get(uid);

            return 1;
        }
        return null;
    }
}

