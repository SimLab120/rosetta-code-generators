package com.regnosys.rosetta.generators.sample;

import com.google.common.html.HtmlEscapers;

/*
 * Static utility methods for generation
 */
final class GeneratorUtils {

	static final String LINE_SEPARATOR = System.getProperty("line.separator");

	private GeneratorUtils() {
		// suppress instantiation
	}

	static String toGroovyType(String type) {
		switch (type) {
		case "string":
			return "String";
		case "int":
			return "Integer";
		case "number":
			return "BigDecimal";
		case "boolean":
			return "Boolean";
		case "date":
			return "LocalDate";
		case "time":
			return "LocalTime";
		case "dateTime":
			return "LocalDateTime";
		case "Bar":
			return "Bar";
		default:
			return type;
		}
	}

	static String emptyGroovyDocWithVersion(String version) {
		StringBuilder sb = new StringBuilder();
		sb.append("/**").append(LINE_SEPARATOR);
		sb.append(" * @version ").append(version).append(LINE_SEPARATOR);
		sb.append("*/").append(LINE_SEPARATOR);
		return sb.toString();
	}

	static String groovyDocWithVersion(String definition, String version) {
		StringBuilder sb = new StringBuilder();
		sb.append("/**").append(LINE_SEPARATOR);
		if (definition != null) {
			sb.append(" * ").append(definition).append(LINE_SEPARATOR);
			sb.append(" *").append(LINE_SEPARATOR);
		}
		sb.append(" * @version ").append(version).append(LINE_SEPARATOR);
		sb.append("*/");
		return sb.toString();
	}
}
