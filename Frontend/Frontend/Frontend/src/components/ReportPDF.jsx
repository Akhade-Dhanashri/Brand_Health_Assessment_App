import { Page, Text, View, Document, StyleSheet, Image } from '@react-pdf/renderer'

const styles = StyleSheet.create({
  page: {
    padding: 30,
    fontFamily: 'Helvetica'
  },
  header: {
    marginBottom: 20,
    textAlign: 'center'
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 10
  },
  subtitle: {
    fontSize: 12,
    marginBottom: 20,
    color: '#666'
  },
  section: {
    marginBottom: 15
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    marginBottom: 8,
    color: '#2c3e50'
  },
  scoreItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 5
  },
  scoreLabel: {
    fontSize: 12
  },
  scoreValue: {
    fontSize: 12,
    fontWeight: 'bold'
  },
  overallScore: {
    marginTop: 20,
    padding: 15,
    backgroundColor: '#f0f7ff',
    borderRadius: 5
  },
  chartPlaceholder: {
    width: '100%',
    height: 120,
    backgroundColor: '#f5f5f5',
    justifyContent: 'center',
    alignItems: 'center',
    marginVertical: 15,
    fontSize: 10,
    color: '#999'
  },
  recommendations: {
    marginTop: 15,
    fontSize: 12,
    lineHeight: 1.5
  },
  footer: {
    position: 'absolute',
    bottom: 20,
    left: 0,
    right: 0,
    textAlign: 'center',
    fontSize: 8,
    color: '#999'
  }
})

export const ReportPDF = ({ results, date }) => (
  <Document>
    <Page size="A4" style={styles.page}>
      <View style={styles.header}>
        <Text style={styles.title}>Brand Health Assessment Report</Text>
        <Text style={styles.subtitle}>Generated on {date}</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Category Scores</Text>
        {Object.entries(results.categoryScores).map(([category, score]) => (
          <View key={category} style={styles.scoreItem}>
            <Text style={styles.scoreLabel}>{category}</Text>
            <Text style={styles.scoreValue}>
              {score.percentage}% ({score.total}/{score.max} points)
            </Text>
          </View>
        ))}
      </View>

      <View style={styles.chartPlaceholder}>
        <Text>Brand Health Score Visualization</Text>
      </View>

      <View style={styles.overallScore}>
        <Text style={styles.sectionTitle}>Overall Brand Health</Text>
        <Text>
          Your brand achieved an overall score of {results.overallPercentage}% 
          ({results.overallScore}/{results.maxScore} points)
        </Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Recommendations</Text>
        <Text style={styles.recommendations}>
          1. Focus on categories scoring below 70%\n
          2. Conduct employee training for brand alignment\n
          3. Review customer feedback regularly\n
          4. Strengthen brand communication channels\n
          5. Monitor competitor positioning
        </Text>
      </View>

      <View style={styles.footer}>
        <Text>Confidential - Brand Health Assessment Report</Text>
      </View>
    </Page>
  </Document>
)