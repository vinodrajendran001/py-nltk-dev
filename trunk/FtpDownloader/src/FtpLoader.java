import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintWriter;

import org.apache.commons.io.FileUtils;
import org.apache.commons.net.PrintCommandListener;
import org.apache.commons.net.ftp.FTP;
import org.apache.commons.net.ftp.FTPClient;
import org.apache.commons.net.ftp.FTPClientConfig;
import org.apache.commons.net.ftp.FTPConnectionClosedException;
import org.apache.commons.net.ftp.FTPFile;
import org.apache.commons.net.ftp.FTPReply;
import org.apache.commons.net.io.CopyStreamEvent;
import org.apache.commons.net.io.CopyStreamListener;


public class FtpLoader {

	private static CopyStreamListener createListener(){
        return new CopyStreamListener(){
            private long megsTotal = 0;
            
            @Override
            public void bytesTransferred(CopyStreamEvent event) {
                bytesTransferred(event.getTotalBytesTransferred(), event.getBytesTransferred(), event.getStreamSize());
            }

            @Override
            public void bytesTransferred(long totalBytesTransferred, int bytesTransferred, long streamSize) {
                long megs = totalBytesTransferred / (1024*1024);
                for (long l = megsTotal; l < megs; l++) {
                    System.err.print("#");
                }
                megsTotal = megs;
            }
        };
    }

	public static void main(String[] args) {
		FTPClient ftp = null;
		try {
			if (!System.getProperty("java.version").startsWith("1.6.")) {
				Utils.log("WARNING: this program requirea Java 1.6 but not newer!");
			}
			
			String url = Utils.getParam("url");
			int port = Utils.getIntParam("port"); 
			String downloads = Utils.getParam("downloads");
			String ftpPath = Utils.getParam("ftpPath");
			
			Utils.log("Connecting to: " + url + ", port: " + port);
			ftp = new FTPClient();
			ftp.setListHiddenFiles(false);
			ftp.setCopyStreamListener(createListener());
			ftp.setConnectTimeout(10000);
			ftp.setDefaultTimeout(1000);
			
			// suppress login details
	        ftp.addProtocolCommandListener(new PrintCommandListener(new PrintWriter(System.err), true));
	        ftp.connect(url, port);
	        ftp.setSoTimeout(10000);
	        
			if (!FTPReply.isPositiveCompletion(ftp.getReplyCode())) {
				Utils.log("FTP server refused connection, bad reply code = " + ftp.getReplyCode());
				ftp.disconnect();
			}
			
			Utils.log("Connected successfully");
			
			 
			if (!ftp.login(Utils.getParam("username"), Utils.getParam("password"))) {
				Utils.log("Failure login in with given credentials");
			} else {
				
				Utils.log("Remote system is " + ftp.getSystemType());
				
				ftp.setFileType(FTP.BINARY_FILE_TYPE);
				ftp.enterLocalPassiveMode();
				
				// lenient - list files
                FTPClientConfig config = new FTPClientConfig();
                config.setLenientFutureDates(true);
                ftp.configure(config );

                Utils.log("Download directory: " + downloads);
                FileUtils.deleteDirectory(new File(downloads));

                downloadDirectory(ftp, ftpPath, "", downloads);
			}
			 
			ftp.logout();
			Utils.log("Ok, job done, check folder: " + downloads);
			
		} catch (FTPConnectionClosedException e) {
			Utils.log("Server closed connection", e);
		} catch (Exception e) {
			Utils.log("Exception occured", e);
		} finally {
			if (ftp != null && ftp.isConnected()) {
                try {
                    ftp.disconnect();
                } catch (IOException fe) {
                	Utils.log("Failure closing FTP connection", fe);
                }
            }
		}
		
	}

	private static void downloadDirectory(FTPClient ftp, String base, String path, String to) throws Exception {
		Utils.log("Downloading files from: " + base + path);

        for (FTPFile f: ftp.listFiles(base + path)) {
			if (f.isFile()) {
				String dest = path + "/" + f.getName();
				OutputStream output = new FileOutputStream(to + dest);
				ftp.retrieveFile(base + dest, output);
				output.close();
				Utils.log("Fetch file: " + base + dest);
			} else if (f.isDirectory() && !".".equals(f.getName()) && !"..".equals(f.getName())) {
				String dest = path + "/" + f.getName();
				File fp = new File(to + dest);
				fp.mkdirs();
				downloadDirectory(ftp, base, dest, to);
			}
		}
	}

}
