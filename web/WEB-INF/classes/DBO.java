import java.sql.SQLException;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;
import java.sql.DriverManager;

public class DBO {
	private static String driverName = "org.apache.hive.jdbc.HiveDriver";
	
	private Statement stmt;
	static private DBO instance = null;

	static public DBO getInstance(){
		if(instance == null){
			try{
				instance = new DBO();
			} catch (SQLException e){
				e.printStackTrace();
			}
		}

		return instance;
	}
	
	private DBO() throws SQLException{
		try{
			Class.forName(driverName);
		} catch (ClassNotFoundException e){
			e.printStackTrace();
			System.exit(1);
		}
		
		Connection con = DriverManager.getConnection("jdbc:hive2://master:10000", "hdp", "hdp");
		stmt = con.createStatement();
		try{
			stmt.execute("use team02");
		} catch (SQLException e){
			e.printStackTrace();
		}
	}
	
	public ResultSet query(String str){
		try {
			return stmt.executeQuery(str);
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return null;
	}

	static public void main(String argvs[]){
	//	try {
	//		DBO dbo = new DBO();
	//		ResultSet rs = dbo.query("select * from dim_brand");
	//		while(rs.next()){
	//			System.out.println(rs.getString(1));
	//		}
	//	} catch (SQLException e) {
	//		e.printStackTrace();
	//	}
		try{
			DBO dbo = DBO.getInstance();
			String sql_all_cars = "select brand_name, serial, yearType, volumn, carStyle,"+ 
					"deal_date, post_date, prov_name, city_name,"+
					"guide_price, total_price, year_discount, url from rpt_price limit 5";
			ResultSet rs = dbo.query(sql_all_cars);
			while(rs.next()){
				System.out.println(rs.getString(1));
			}
		} catch (SQLException e){
			e.printStackTrace();
		}
	}
}
