
import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import java.sql.*;
import java.io.*;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

/**
 * Servlet implementation class FeiguHandler
 */
@WebServlet("/FeiguHandler")
public class FeiguHandler extends HttpServlet {
	private static final long serialVersionUID = 1L;
       	
	//private final String sql_all_cars = "select brand_name, serial, yearType, volumn, carStyle,"+ 
	//				"deal_date, post_date, prov_name, city_name,"+
	//				"guide_price, total_price, year_discount, url from rpt_price limit 5";
    /**
     * @see HttpServlet#HttpServlet()
     */
    public FeiguHandler() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		response.setCharacterEncoding("UTF-8");
		try{
		//	ResultSet rs = DBO.getInstance().query("select brand_name, serial, yearType, volumn, carStyle,deal_date, post_date, prov_name, city_name,guide_price, total_price, year_discount, url from rpt_price limit 5");
			ResultSet rs = DBO.getInstance().query("select * from rpt_price");
			ResultSetMetaData metaData = rs.getMetaData();
			int column = metaData.getColumnCount();

			JSONArray json = new JSONArray();

			while(rs.next()){
				JSONObject obj = new JSONObject();
				for(int i = 1; i <= column; i ++){
					String columnName = metaData.getColumnLabel(i);
					String value = rs.getString(columnName);
					obj.put(columnName, value);
				}
				json.add(obj);
			}
			response.getWriter().append(json.toString());
		}catch(Exception e){
			e.printStackTrace();
		}
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		doGet(request, response);
	}
}
