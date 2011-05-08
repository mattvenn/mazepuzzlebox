import processing.core.*; 
import processing.xml.*; 

import java.applet.Applet; 
import java.awt.*; 
import java.net.*; 

import java.applet.*; 
import java.awt.Dimension; 
import java.awt.Frame; 
import java.awt.event.MouseEvent; 
import java.awt.event.KeyEvent; 
import java.awt.event.FocusEvent; 
import java.awt.Image; 
import java.io.*; 
import java.net.*; 
import java.text.*; 
import java.util.*; 
import java.util.zip.*; 
import java.util.regex.*; 

public class webredirect extends PApplet {






  private TextField searchField;
  protected String baseURL, serviceName, frame="Results";
  protected int textFieldSize = 30;
String inputFromPage;
  public void setup() {

    size( 400,400);
   inputFromPage = getParameter("Message");
    baseURL = "http://search.yahoo.com/bin/search?p=";
    serviceName = "Yahoo";
    Panel inputPanel = new Panel();
    inputPanel.add(new Label("Search String: "));
    searchField = new TextField(textFieldSize);
    inputPanel.add(searchField);
  println( "got input: " + inputFromPage );
    add(inputPanel);
    add(new Button("Submit to " + serviceName));
  }
public void draw()
{
  
}

  public boolean action(Event event, Object object) {
//    String searchString  = URLEncoder.encode(searchField.getText());
  String searchString = inputFromPage;
    showSearch(searchString);
   
    return(true);
  }

  public void showSearch(String searchString) {
    try {
      URL url = new URL(baseURL + searchString);
      getAppletContext().showDocument(url);
    } catch(MalformedURLException mue) {
      System.out.println("Illegal URL: " + baseURL
                         + searchString);
    }
  }

  static public void main(String args[]) {
    PApplet.main(new String[] { "--bgcolor=#DFDFDF", "webredirect" });
  }
}
