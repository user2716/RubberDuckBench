import java.util.ArrayList;

class LogFilePath {

    private final String mPrefix;
    private final String mTopic;

    public LogFilePath(String prefix, String topic) {
        mPrefix = prefix;
        mTopic = topic;
    }

    public String getLogFileParentDir() {
        ArrayList<String> elements = new ArrayList<String>();
        if(mPrefix.length() > 0) { //line in question - should a null check be added?
            elements.add(mPrefix);
        }
        if(mTopic.length() > 0) {
            elements.add(mTopic);
        }
        return String.join("/", elements);
    }

}
