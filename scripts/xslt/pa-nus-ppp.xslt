<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:wb="http://www.worldbank.org">
  <xsl:output method="text" encoding="utf-8" />

  <xsl:param name="delim" select="','" />
  <xsl:param name="quote" select="'&quot;'" />
  <xsl:param name="break" select="'&#xA;'" />

  <xsl:template match="wb:data">
    <xsl:for-each select="wb:data">
      <xsl:if test="wb:value != ''">
        <xsl:variable name="country" select="wb:country" />
        <xsl:value-of select="concat($quote, $country, $quote)" />
        <xsl:value-of select="$delim" />
        <xsl:value-of select="wb:country/@id" />
        <xsl:value-of select="$delim" />
        <xsl:value-of select="wb:date" />
        <xsl:value-of select="$delim" />
        <xsl:value-of select="wb:value" />
        <xsl:value-of select="$break" />
      </xsl:if>
    </xsl:for-each>
  </xsl:template>

  <xsl:template match="text()" />
</xsl:stylesheet>
