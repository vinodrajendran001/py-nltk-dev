import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Properties;


public class Utils {
	
	private static PrintWriter logfile = null;
	private static Properties properties = null;
	
	static {
		try {
			logfile = new PrintWriter("log.txt");
		} catch (Exception e) {
			log("Failure creating log file!");
		}
		
		try {
			properties = new Properties();
			properties.load(new FileReader("config.properties"));
		} catch (Exception e) {
			log("Failure reading config.priperties file!");
		}
	}
	
	public static String getParam(String key) {
		return ((properties != null) ? properties.getProperty(key) : null);
	}
	
	public static Integer getIntParam(String key) {
		return ((properties != null) ? Integer.parseInt(properties.getProperty(key)) : null);
	}
	
	public static void log(String msg, Throwable e, Object... params) {
		log(msg, params);
		e.printStackTrace();
	}
	
	public static void log(String msg, Object... params) {
		SimpleDateFormat sdf = new SimpleDateFormat("[yyyy-MM-dd HH:mm:ss.SSS] ");
		StringBuilder sb = new StringBuilder(sdf.format(new Date()));
		sb.append(msg);
		for(Object o: params){
			sb.append(o);
		}
		System.out.println(sb.toString());
		if (logfile != null) {
			logfile.println(sb.toString());
			logfile.flush();
		}
	}
	
	public static String getPageContents(String url) throws Exception {
		InputStream in = ((new URL(url)).openConnection()).getInputStream();
		BufferedReader reader = new BufferedReader(new InputStreamReader(in));
		StringBuilder sb = new StringBuilder();
		String line = null;
		while ((line = reader.readLine()) != null) {
			sb.append(line);
		}
		reader.close();
		return sb.toString();
	}
	
	public static String getFileContents(String path) throws Exception {
		BufferedReader reader = new BufferedReader(new FileReader(path));
		StringBuilder sb = new StringBuilder();
		String line = null;
		while ((line = reader.readLine()) != null) {
			sb.append(line);
		}
		reader.close();
		return sb.toString();
	}
	
	public static void saveAsFile(String filename, String content) throws Exception {
		PrintWriter writer = new PrintWriter(new File(filename));
		writer.write(content);
		writer.close();
	}
}
