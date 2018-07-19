package cn.com.transcosmos;

import java.sql.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.lang.reflect.*;
import java.math.BigDecimal;

/**
*  应用Oracle JDBC 驱动操作类， 在构造器中传入连接URL。
*  开放接口如下：
* 	connect: 连接数据库，执行所有操作之前必须的第一步。关闭了自动提交
* 	insert: 根据提供的表名获得各个列的数据类型，为sql模版的参数进行格式化设值，循环插入数据。
* 			出错时rollback
* 	select: 执行SQL文，未连接状态执行此方法会出异常信息
* 	commit: 数据插入后进行提交
* 	close: 关闭数据库连接，最后一步操作
*/

public class OracleConnector {
	private Connection conn = null;
	private PreparedStatement preparedStatement = null;

	private String url = null;

	/**
	 * 构造器
	 * @param url 数据库连接url
	 */
	public OracleConnector(String url) {
		this.url = url;
	}

	/**
	 * 连接数据库。
	 * 根据数据库连接url建立数据库连接
	 */
	public void connect() {
		try {
			Class.forName("oracle.jdbc.OracleDriver");
			this.conn = DriverManager.getConnection(this.url);
			this.conn.setAutoCommit(false);
			System.out.println("Oracle Driver: Connect Success");
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
			System.out.println("Oracle Driver: Couldn't find the Driver jar");
		} catch (SQLException e) {
			e.printStackTrace();
			System.out.println("Oracle Driver: Cannot Connected to the DataBase");
		}
	}

	/**
	 * 向数据库插入数据
	 * 1. 先向数据库做简单请求验证连接，并从请求的元数据中获取列定义，
	 * 2. 创建请求sql模板
	 * 3. 依据列定义，迭代数据列表，向模板中插入参数
	 * 4. 迭代dataList，按行执行插入SQL
	 * @param tableName		表名
	 * @param columnsList	列名列表
	 * @param dataList		数据二维列表
	 * @return	返回插入结果。0 为失败， 1 为成功
	 */
	public int[] insert(String tableName, List<String> columnsList, List<List<Object>> dataList) {
		// 测试请求数据库
		ResultSet testResult = null;
		StringBuilder testSql = new StringBuilder();
		testSql.append("select ").append(String.join(", ", columnsList)).append(" from \"").append(tableName).append("\"")
			.append("where rownum = 1");
		try {
			this.preparedStatement = this.conn.prepareStatement(testSql.toString());
			testResult = this.preparedStatement.executeQuery();
		} catch (SQLException e) {
			e.printStackTrace();
			System.out.println("Oracle Driver: Error In Execute SQL");
			this.close();
		}

		// 获取目标表的列定义
		List<Integer> columnsTypeList = new ArrayList<>();
		try {
			int columnCounts = testResult.getMetaData().getColumnCount();
			for (int i = 1; i <= columnCounts; i ++) {
				columnsTypeList.add(testResult.getMetaData().getColumnType(i));
			}
			System.out.println(columnsTypeList);
		} catch (SQLException e) {
			e.printStackTrace();
			System.out.println("Oracle Driver: SQL Error in get testResult's metadata");
			this.close();
		}
		// 生成SQL模板
		StringBuilder insertSqlTemplate = new StringBuilder();
		String[] placeholderArr = new String[columnsList.size()];
		Arrays.fill(placeholderArr, "?");
		insertSqlTemplate.append("insert into \"").append(tableName).append("\" (").append(String.join(", ", columnsList)).append(") ")
			.append("values (").append(String.join(", ", Arrays.asList(placeholderArr))).append(")");

		// 迭代dataList，向模板中插入参数并打印请求内容，执行SQL
		List<Object> paramList = new ArrayList<>();
		int[] result = null;
		try {
			for (List<Object> dataRow: dataList) {
				this.preparedStatement = this.conn.prepareStatement(insertSqlTemplate.toString());
				for (int colCount = 0; colCount < dataRow.size(); colCount++) {
					if (dataRow.get(colCount) == null) {
						this.preparedStatement.setNull(colCount + 1, columnsTypeList.get(colCount));
						paramList.add(null);
					} else {
						Class<?> type = this.switchType(columnsTypeList.get(colCount));
						Object param = this.prepareParam(type, dataRow.get(colCount));
						this.getDynamicMethod(type).invoke(this.preparedStatement, colCount + 1, param);
						paramList.add(param);
					}
				}
				System.out.println("Execute: " + insertSqlTemplate.toString());
				System.out.println(" Params: " + paramList.toString());
				this.preparedStatement.addBatch();
			}
			result = this.preparedStatement.executeBatch();
			this.commit();
		} catch (Exception e) {
			// 发生异常时回滚并关闭数据库连接
			e.printStackTrace();
			System.out.println("Oracle Driver: SQL Error in execute insert");
			this.rollback();
			this.close();
		}
		return result;
	}

	/**
	 * 按照输入的类型，将原数据进行转型
	 * @param type	数据类型
	 * @param data	原数据
	 * @return			处理后数据
	 */
	private Object prepareParam(Class<?> type, Object data) {
		Object resultParam = null;
		if (data == null) return data;
		try {
			if (type == BigDecimal.class) {
				return new BigDecimal(data.toString());
			} else if (type == String.class) {
				resultParam = type.getMethod("valueOf", Object.class).invoke(null, data);
			} else {
				resultParam = type.getMethod("valueOf", String.class).invoke(null, data.toString());
			}
		} catch (IllegalAccessException | IllegalArgumentException | InvocationTargetException
				| NoSuchMethodException | SecurityException e) {
			System.out.println("Oracle Driver: SQL Error in parse params list");
			e.printStackTrace();
			this.close();
		}
		return resultParam;
	}

	/**
	 * 根据输入的类型，动态取得"java.sql.PreparedStatement"中的类型方法。
	 * Class<java.lang.String> -> setString(index, data);
	 * @param type	类型
	 * @return			获得的方法
	 */
	private Method getDynamicMethod(Class<?> type) {
		String methodName = "set" + type.getSimpleName();
		Class<?> paramType = type;
		// Integer对应的方法名为setInt，特殊处理
		if (type.getSimpleName() == "Integer") {
			methodName = "setInt";
			paramType = Integer.class;
		}

		// 利用反射动态取得方法，getMethod的第二个参数为列索引的参数(后面的index)： setString(index, data)
		Method resultMethod = null;
		try {
			resultMethod = Class.forName("java.sql.PreparedStatement").getMethod(methodName, int.class, paramType);
		} catch (NoSuchMethodException | SecurityException | ClassNotFoundException e) {
			System.out.println("Oracle Driver: SQL Error in dynamicCall the methods of statement");
			e.printStackTrace();
			this.close();
		}
		return resultMethod;
	}

	/**
	 * 选择类型code选择类型
	 * @param typeCode	类型code
	 * @return					类型class
	 */
	private Class<?> switchType(int typeCode) {
		switch (typeCode) {
			case Types.VARCHAR:
			case Types.CHAR:
			case Types.NCHAR:
			case Types.NVARCHAR:
			case Types.LONGNVARCHAR:
			case Types.LONGVARCHAR:
				return String.class;
			case Types.INTEGER:
				return Integer.class;
			case Types.BIGINT:
				return Long.class;
			case Types.BOOLEAN:
				return Boolean.class;
			case Types.NUMERIC:
			case Types.DECIMAL:
				return BigDecimal.class;
			case Types.DOUBLE:
				return Double.class;
			case Types.FLOAT:
				return Float.class;
			case Types.DATE:
				return Date.class;
			case Types.TIME:
			case Types.TIME_WITH_TIMEZONE:
				return Time.class;
			case Types.TIMESTAMP:
			case Types.TIMESTAMP_WITH_TIMEZONE:
				return Timestamp.class;
			default:
				return String.class;
		}
	}

	/**
	 * 执行SELECT数据的SQL文，获取结果
	 * @param sql	SELECT数据的SQL文
	 * @return		结果键值对的List
	 */
	public List<Map<String, Object>> select(String sql) {
		// 请求数据
		ResultSet result = null;
		try {
			this.preparedStatement = this.conn.prepareStatement(sql);
			result = this.preparedStatement.executeQuery();
		} catch (SQLException e) {
			e.printStackTrace();
			System.out.println("Oracle Driver: Error In Execute SQL");
			this.close();
		}

		// 获取列数
		List<Map<String, Object>> resultList = new ArrayList<>();
		int columnCounts = 0;
		try {
			columnCounts = result.getMetaData().getColumnCount();
		} catch (SQLException e) {
			e.printStackTrace();
			System.out.println("Oracle Driver: SQL Error in get Column count");
			this.close();
		}

		// 循环列数，根据列索引获取表头，格式化结果集
		try {
			while (columnCounts > 0 && result.next()) {
				Map<String, Object> lineMap = new HashMap<>();
				for (int i = 1; i <= columnCounts; i ++) {
					String columnLabel = result.getMetaData().getColumnLabel(i);
					lineMap.put(columnLabel, result.getObject(columnLabel));
				}
				resultList.add(lineMap);
			}
		} catch (SQLException e) {
			e.printStackTrace();
			System.out.println("Oracle Driver: SQL Error in parse ResultSet");
			this.close();
		}
		return resultList;
	}

	/**
	 * 封装回滚动作
	 */
	private void rollback() {
		try {
			this.conn.rollback();
		} catch (SQLException e) {
			e.printStackTrace();
			System.out.println("Oracle Driver: Error In rollback the connector");
			this.close();
		}
	}

	/**
	 * 数据提交操作封装
	 */
	public void commit() {
		try {
			this.conn.commit();
		} catch (SQLException e) {
			e.printStackTrace();
			System.out.println("Oracle Driver: Error In Commit the Query");
			this.close();
		}
	}

	/**
	 * 关闭数据库连接
	 */
	public void close() {
		if (this.conn == null || this.preparedStatement == null) return;
		try {
			if (this.preparedStatement.isClosed()) this.preparedStatement.close();
			if (this.conn.isClosed()) this.conn.close();
		} catch (SQLException e) {
			e.printStackTrace();
			System.out.println("Oracle Driver: Error In close the connection");
		}
	}

	/**
	 * Just For example
	 * connect to the Oracle Database and query sql for result.
	 * @param args
	 * 		args[0] is the connectable URL
	 * 		args[1] is the queriable SQL
	 * @return the result of this query
	 */
	public static void main(String[] args) {
		System.out.print("Hello World");
	}

}
