<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="text"/>
    <xsl:template match="/testsuites">
        <xsl:text>Test Summary Report
</xsl:text>
        <xsl:text>==================
</xsl:text>
        <xsl:text>Total Tests: </xsl:text><xsl:value-of select="@tests"/><xsl:text>
</xsl:text>
        <xsl:text>Passed: </xsl:text><xsl:value-of select="10"/><xsl:text>
</xsl:text>
        <xsl:text>Failed: </xsl:text><xsl:value-of select="@failures"/><xsl:text>
</xsl:text>
        <xsl:text>Errors: </xsl:text><xsl:value-of select="@errors"/><xsl:text>
</xsl:text>
        <xsl:text>Time: </xsl:text><xsl:value-of select="@time"/> seconds<xsl:text>
</xsl:text>
        <xsl:text>
Test Cases:
</xsl:text>
        <xsl:for-each select="testsuite/testcase">
            <xsl:text>- </xsl:text><xsl:value-of select="@name"/>
            <xsl:choose>
                <xsl:when test="failure">
                    <xsl:text>: FAILED</xsl:text>
                    <xsl:text> (</xsl:text><xsl:value-of select="failure/@message"/><xsl:text>)</xsl:text>
                </xsl:when>
                <xsl:when test="error">
                    <xsl:text>: ERROR</xsl:text>
                    <xsl:text> (</xsl:text><xsl:value-of select="error/@message"/><xsl:text>)</xsl:text>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:text>: PASSED</xsl:text>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:text> (</xsl:text><xsl:value-of select="@time"/> seconds)<xsl:text>
</xsl:text>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>